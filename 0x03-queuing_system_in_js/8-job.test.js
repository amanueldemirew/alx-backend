import { expect } from 'chai';
import kue from 'kue';
import createPushNotificationsJobs from './8-job';

describe('createPushNotificationsJobs', () => {
  let queue;

  beforeEach(() => {
    queue = kue.createQueue();
    queue.testMode.enter();
  });

  afterEach(() => {
    queue.testMode.clear();
    queue.testMode.exit();
  });

  it('should display an error message if jobs is not an array', () => {
    expect(() => createPushNotificationsJobs({}, queue)).to.throw('Jobs is not an array');
  });

  it('should create new jobs in the queue', () => {
    const jobs = [
      {
        phoneNumber: '4153518780',
        message: 'This is the code 1234 to verify your account',
      },
      {
        phoneNumber: '4153518781',
        message: 'This is the code 5678 to verify your account',
      },
    ];

    createPushNotificationsJobs(jobs, queue);

    const jobCount = queue.testMode.jobs.length;
    expect(jobCount).to.equal(jobs.length);
  });
});
