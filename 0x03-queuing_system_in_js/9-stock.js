const listProducts = [
  {
    id: 1, name: 'Suitcase 250', price: 50, stock: 4,
  },
  {
    id: 2, name: 'Suitcase 450', price: 100, stock: 10,
  },
  {
    id: 3, name: 'Suitcase 650', price: 350, stock: 2,
  },
  {
    id: 4, name: 'Suitcase 1050', price: 550, stock: 5,
  },
];

function getItemById(id) {
  return listProducts.find((product) => product.id === id);
}

const express = require('express');

const app = express();
const port = 1245;

app.get('/list_products', (req, res) => {
  res.json(listProducts.map((product) => ({
    itemId: product.id,
    itemName: product.name,
    price: product.price,
    initialAvailableQuantity: product.stock,
  })));
});

app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});

const redis = require('redis');
const { promisify } = require('util');

const client = redis.createClient();
const getAsync = promisify(client.get).bind(client);
const setAsync = promisify(client.set).bind(client);

function reserveStockById(itemId, stock) {
  const key = `item.${itemId}`;
  return setAsync(key, stock);
}

async function getCurrentReservedStockById(itemId) {
  const key = `item.${itemId}`;
  const stock = await getAsync(key);
  return stock ? parseInt(stock, 10) : 0;
}

app.get('/list_products/:itemId', async (req, res) => {
  const itemId = parseInt(req.params.itemId, 10);
  const product = getItemById(itemId);

  if (!product) {
    res.status(404).json({ status: 'Product not found' });
  } else {
    const currentQuantity = await getCurrentReservedStockById(itemId);
    res.json({
      itemId: product.id,
      itemName: product.name,
      price: product.price,
      initialAvailableQuantity: product.stock,
      currentQuantity,
    });
  }
});

app.get('/reserve_product/:itemId', async (req, res) => {
  const itemId = parseInt(req.params.itemId, 10);
  const product = getItemById(itemId);

  if (!product) {
    res.status(404).json({ status: 'Product not found' });
  } else {
    const currentQuantity = await getCurrentReservedStockById(itemId);

    if (currentQuantity === 0) {
      res.json({ status: 'Not enough stock available', itemId: product.id });
    } else {
      await reserveStockById(itemId, currentQuantity - 1);
      res.json({ status: 'Reservation confirmed', itemId: product.id });
    }
  }
});
