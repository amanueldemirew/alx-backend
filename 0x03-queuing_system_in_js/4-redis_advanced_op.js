import redis from 'redis';

const client = redis.createClient();

client.on('error', (err) => {
  console.log('Redis client not connected to the server:', err);
});

client.on('connect', () => {
  console.log('Redis client connected to the server');
});

const hashKey = 'HolbertonSchools';
const hashValues = {
  Portland: '50',
  Seattle: '80',
  'New York': '20',
  Bogota: '20',
  Cali: '40',
  Paris: '2',
};

Object.entries(hashValues).forEach(([key, value]) => {
  client.hset(hashKey, key, value, redis.print);
});

client.hgetall(hashKey, (err, result) => {
  if (err) {
    console.error('Error getting hash: ', err);
    return;
  }
  console.log(result);
});
