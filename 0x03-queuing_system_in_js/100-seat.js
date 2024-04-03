import express from 'express';
import redis from 'redis';
import kue from 'kue';
import { promisify } from 'util';

const initialSeatsCount = 50;
let reservationEnabled = true;
const port = 1245;

const app = express();

const client = redis.createClient();

const queue = kue.createQueue();

const getAsync = promisify(client.get).bind(client);
const setAsync = promisify(client.set).bind(client);

async function reserveSeat(number) {
  await setAsync('available_seats', number);
}

async function getCurrentAvailableSeats() {
  const currentAvailableSeats = await getAsync('available_seats');

  return currentAvailableSeats ? parseInt(currentAvailableSeats, 10) : 0;
}

async function resetAvailableSeats(initialSeatsCount) {
  await setAsync('available_seats', Number.parseInt(initialSeatsCount, 10));
}

app.get('/available_seats', (_, res) => {
  getCurrentAvailableSeats()
    .then((numberOfAvailableSeats) => {
      res.json({ numberOfAvailableSeats });
    });
});

app.get('/reserve_seat', (_, res) => {
  if (!reservationEnabled) {
    res.json({ status: 'Reservation are blocked' });
    return;
  }

  const job = queue.create('reserve_seat').save((err) => {
    if (err) {
      res.json({ status: 'Reservation failed' });
    } else {
      res.json({ status: 'Reservation in process' });
    }
  });

  job.on('complete', () => {
    console.log(`Seat reservation job ${job.id} completed`);
  });

  job.on('failed', (err) => {
    console.log(`Seat reservation job ${job.id} failed: ${err}`);
  });
});

app.get('/process', (_, res) => {
  res.json({ status: 'Queue processing' });

  queue.process('reserve_seat', async (_job, done) => {
    const availableSeats = await getCurrentAvailableSeats();
    const seats = Number.parseInt(availableSeats || 0, 10);

    if (seats > 0) {
      await reserveSeat(seats - 1);
      done();
    } else {
      reservationEnabled = false;
      done(new Error('Not enough seats available'));
    }
  });
});

app.listen(port, () => {
  resetAvailableSeats(initialSeatsCount)
    .then(() => {
      reservationEnabled = true;
      console.log(`API available on localhost port ${port}`);
    });
});
