const createPushNotificationsJobs = (jobs, queue) => {
  if (!Array.isArray(jobs)) {
    return new Error("Jobs is not an array");
  }
  jobs.forEach((element) => {
    const job = queue
      .create("push_notification_code_3", element)
      .save(function (err) {
        if (!err) console.log(`Notification job created: ${job.id}`);
      });

    job.on("complete", () =>
      console.log(`Notification job ${job.id} completed`)
    );
    job.on("failed", (errorMessage) =>
      console.log(`Notification job ${job.id} failed: ${errorMessage}`)
    );
    job.on("progress", (progress) =>
      console.log(`Notification job ${job.id}  ${progress}% complete`)
    );
  });
};

export default createPushNotificationsJobs;
