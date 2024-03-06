const express = require("express");
import { createClient } from "redis";
import { promisify } from "util";

const client = createClient();
client
  .on("connect", () => console.log("Redis client connected to the server"))
  .on("error", (err) =>
    console.log(`Redis client not connected to the server: ${err}`)
  );

const getStock = promisify(client.get).bind(client);

const listProducts = [
  { Id: 1, name: "Suitcase 250", price: 50, stock: 4 },
  { Id: 2, name: "Suitcase 450", price: 100, stock: 10 },
  { Id: 3, name: "Suitcase 650", price: 350, stock: 2 },
  { Id: 4, name: "Suitcase 1050", price: 550, stock: 5 },
];

const getItemById = (id) => {
  return listProducts.find((item) => item.Id === id);
};

const reserveStockById = (itemId, stock) => {
  client.set(itemId, stock);
};

const getCurrentReservedStockById = async (itemId) => {
  const stok = await getStock(itemId);
  return stok;
};
const app = express();
const port = 1245;

app.get("/list_products", (req, res) => {
  res.status(200).json(listProducts);
});

app.get("/list_products/:itemId", async (req, res) => {
  const { itemId } = req.params;
  const item = getItemById(parseInt(itemId));
  if (item === undefined) {
    return res.json({ status: "Product not found" });
  }
  const stock = await getCurrentReservedStockById(itemId);
  const new_item = {
    itemId: item.Id,
    itemName: item.name,
    price: item.price,
    initialAvailableQuantity: item.stock,
    currentQuantity: stock ? parseInt(stock) : item.stock,
  };
  res.json(new_item);
});

app.get("/reserve_product/:itemId", async (req, res) => {
  const { itemId } = req.params;
  const item = getItemById(parseInt(itemId));
  if (item === undefined) {
    return res.json({ status: "Product not found" });
  }

  const stock = await getCurrentReservedStockById(itemId);
  if (stock !== null) {
    if (parseInt(stock) === 0) {
      return res.json({ status: "Not enough stock available", itemId: itemId });
    }
    reserveStockById(itemId, parseInt(stock) - 1);
    return res.json({ status: "Reservation confirmed", itemId: itemId });
  } else {
    reserveStockById(itemId, item.stock - 1);
    return res.json({ status: "Reservation confirmed", itemId: itemId });
  }
});

app.listen(port, () => {
  console.log(`API available on localhost port ${port}`);
});

module.exports = app;
