/**
 * Responds to any HTTP request.
 *
 * @param {!express:Request} req HTTP request context.
 * @param {!express:Response} res HTTP response context.
 */
exports.getNames = (req, res) => {
  console.log('req is', req)
  if (req.method === 'OPTIONS') {
    res.setHeader('Access-Control-Allow-Origin', '*')
    res.setHeader('Access-Control-Allow-Methods', 'GET')
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type')
    res.setHeader('Access-Control-Max-Age', '3600')
    res.status(204).send();
  } else {
  
    var axios = require('axios');
    var data = JSON.stringify({
      "collection": "people_records",
      "database": "listing",
      "dataSource": "listing",
      "projection": {
        "_id": 0
      }
    });
                
    var config = {
      method: 'post',
      url: 'https://data.mongodb-api.com/app/data-jtywc/endpoint/data/beta/action/find',
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Request-Headers': '*',
        'api-key': 'Ubvb0Ge4BIheJQV8dA1a91pZv7fUfCNhaaag0QvgutWu2ox8jQT5xk3YidlbQYc1'
      },
      data : data
    };
                
    axios(config)
      .then(function (response) {
          console.log(JSON.stringify('response.data is', response.data));
          // let message = req.query.message || req.body.message || 'Hello World!';
          console.log('message is', response.data, 'type: ', typeof response.data);
          res.setHeader('Access-Control-Allow-Origin', '*')
          res.status(200).send(response.data);
      })
      .catch(function (error) {
          console.log(error);
      });
  }
};

exports.main = function() {
  const req = {
      method: "POST"
  }
  const res = "Hello World"

  this.getNames(req, res)
}