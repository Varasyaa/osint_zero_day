// filename: censys.js
const axios = require("axios");

const censysAPI = async (ip) => {
  const url = `https://search.censys.io/api/v2/hosts/${ip}`;
  const headers = {
    "Authorization": `Basic ${Buffer.from("UID:SECRET").toString("base64")}`
  };
  const res = await axios.get(url, { headers });
  return res.data;
};

module.exports = censysAPI;
