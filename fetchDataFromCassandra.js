// Define the function in the MongoDB shell
db.system.js.save({
    _id: "fetchDataFromCassandra",
    value: function() {
        const http = require('http'); // Only available in certain environments

        const options = {
            hostname: 'localhost',
            port: 8000,
            path: '/products/id-with-invoices',
            method: 'GET'
        };

        const req = http.request(options, function(res) {
            const body = '';

            res.on('data', function(chunk) {
                body += chunk;
            });

            res.on('end', function() {
                var data = JSON.parse(body);
                processCassandraData(data);
            });
        });

        req.on('error', function(e) {
            print('Problem with request: ' + e.message);
        });

        req.end();

        function processCassandraData(data) {
            for (var i = 0; i < data.length; i++) {
                let id = data[i];
                ids.push(id);
            }

            return db.products.find({ product_id: { $in: ids }})
        }
    }
});
