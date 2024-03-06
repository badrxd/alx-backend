const redis = require("redis");
import { promisify } from "util";
const kue = require("kue");
const express = require("express");

const client = redis.createClient();
const app = express();
const queue = kue.createQueue();

function reserveSeat(number) {
  client.set("available_seats", number);
}

const get = promisify(client.get).bind(client);

async function getCurrentAvailableSeats() {
  return await get("available_seats");
}

reserveSeat(50);
let reservationEnabled = true;

app.get("/available_seats", (req, res) => {
  getCurrentAvailableSeats().then((resp) =>
    res.json({ numberOfAvailableSeats: resp })
  );
});

app.get("/reserve_seat", (req, res) => {
  if (!reservationEnabled) res.json({ status: "Reservation are blocked" });
  else {
    let job = queue.create("reserve_seat");
    job
      .on("complete", () =>
        console.log(`Seat reservation job ${job.id} completed`)
      )
      .on("failed", (err) =>
        console.log(`Seat reservation job ${job.id} failed: ${err}`)
      )
      .save((err) => {
        if (err) res.json({ status: "Reservation failed" });
        else res.json({ status: "Reservation in process" });
      });
  }
});

app.get("/process", (req, res) => {
  queue.process("reserve_seat", (job, done) => {
    getCurrentAvailableSeats().then((resp) => {
      if (resp == 1) reservationEnabled = false;
      if (resp >= 1) {
        reserveSeat(resp - 1);
        done();
      } else done(new Error("Not enough seats available"));
    });
  });
  res.json({ status: "Queue processing" });
});

const port = 1245;
app.listen(port, () => {
  console.log(`app is listening http://localhost:${port}`);
});
