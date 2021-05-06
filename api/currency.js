require('dotenv').config();
const fetch = require('node-fetch');

module.exports = (req, res) => {
  const base_url = "https://free.currconv.com/api/v7/convert?q=USD_ILS,ILS_USD&compact=ultra&apiKey=";
  const api_key = process.env.CURRENCY_API_KEY;

  get_rates = async () => {
    try {
      const response = await fetch(base_url + api_key);
      const data = await response.json();
      return res.send(data);
    } catch (err) {
      console.error(err);
      return res.send({status: "error"});
    }
  }
  get_rates();
}
