import { createClient, print } from "redis";

const client = createClient();

client
  .on("connect", () => console.log("Redis client connected to the server"))
  .on("error", (err) =>
    console.log(`Redis client not connected to the server: ${err}`)
  );

const setNewSchool = (schoolName, value) => {
  client.set(schoolName, value, print);
};

const displaySchoolValue = (schoolName) => {
  //   const data = client.get(schoolName);
  //   data !== false ? console.log(data) : null;
  client.get(schoolName, (err, res) => {
    if (err) {
      console.log(err);
      return;
    }
    console.log(res);
  });
};

displaySchoolValue("Holberton");
setNewSchool("HolbertonSanFrancisco", "100");
displaySchoolValue("HolbertonSanFrancisco");
