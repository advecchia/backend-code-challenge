# Performance Tests

### <a id="toc"></a>Table of Contents 
 * [Go back to home](https://github.com/advecchia/backend-code-challenge/blob/master/README.md)  
 * [Test 1](#test-1)  
 * [Test 2](#test-2)
 * [Test 3](#test-3)  
 * [Test 4](#test-4)  
 * [Test 5](#test-5)    

A set of performance tests are performed with [LOCUST](http://locust.io/).

To run locally use (after setup your environment):  
$ locust -f backend-code-challenge/tests/performance.py --host=http://0.0.0.0:5000  

To run over my deployed instance use the below command:  
$ locust -f backend-code-challenge/tests/performance.py --host=http://guarded-plateau-54331.herokuapp.com  

You can now access a web interface to execute the performance test, there you can add manually two parameters, the max number of concurrent users and the user spawn per second. Access http://127.0.0.1:8089/ in the browser of your preference and enjoy!  

---  

To show API resilience, I make a variation of simulation parameters. The challenge describe that each vehicle can emit a GPS signal at every 20 seconds, so in this performance test I use the same approach for spawned users accessing the API endpoints. Also I defined a distribution over endpoint access:

| API Endpoint  | HTTP Method           | Demand  | Description
| ------------- |:-------------: | :-----:| -------------
| /      | GET | 5% | Website Home showing the project README.
| /api/v1/emissions      | GET      |   5% | API that allow to get a paginated list of emissions.
| /api/v1/emissions      | POST      |   80% | API that allow insertion of emissions.
| /api/v1/emissions/vehicles/<uuid:id>      | GET      |   5% | API that allow to get a list of emissions by some vehicle.
| /api/v1/emissions/vehicles/type/<string:type>      | GET      |   5% | API that allow to get a list of emissions by some vehicle type.

Below you can see the results for experiments for at least 10 accumulated sequential runs. The title indicates the input parameters for performance framework, in each experiment the first table represents the final request statistics, the second table show the growing value of request distribution over time response. The time columns are measured in milliseconds.

If you take care of failures, you can see that in the majority of the cases the failure rate is below 1% but they occurs, and in general are occasioned by request connection limits, like the below line error:

> ConnectionError(MaxRetryError("HTTPConnectionPool(host='guarded-plateau-54331.herokuapp.com', port=80): Max retries exceeded with url: / (Caused by NewConnectionError('<requests.packages.urllib3.connection.HTTPConnection object at 0x7f37f4416090>: Failed to establish a new connection: [Errno -2] Name or service not known',))",),)  

## Test 1 <a id="test-1"></a> [^](#toc "To top")  
**Max users concurrently = 100, Spawned users per second = 50**  
Method|Name|# requests|# failures|Median response time|Average response time|Min response time|Max response time|Average Content Size|Requests/s
| ------------- |------------- | :-----:| :-----:| :-----:| :-----:| :-----:| :-----:| :-----:| :-----:|
GET|/|33|0|320|512|192|1396|1313|0.25
GET|/api/v1/emissions/|29|0|1000|1103|584|2014|56147|0.22
POST|/api/v1/emissions/|908|3|1100|1184|195|4009|191|6.92
GET|/api/v1/emissions/vehicles/1cc2ed4f-4372-4854-b70c-3206c096b6e9|6|0|550|762|391|1258|22513|0.05
GET|/api/v1/emissions/vehicles/46c791af-0ad0-4e65-9941-bbd8f6156acd|13|0|760|790|386|1435|22575|0.10
GET|/api/v1/emissions/vehicles/b25e7f2c-d34e-4c6f-b4cc-c4fdb7ceecd6|10|0|980|1016|400|1589|22497|0.08
GET|/api/v1/emissions/vehicles/edfde841-177c-4ad9-b640-fbab1404ac79|10|0|620|741|404|1266|22180|0.08
GET|/api/v1/emissions/vehicles/type/bus|7|0|760|883|601|1399|55870|0.05
GET|/api/v1/emissions/vehicles/type/taxi|5|0|1500|1304|667|1646|56148|0.04
GET|/api/v1/emissions/vehicles/type/train|10|0|710|785|586|1237|56415|0.08
GET|/api/v1/emissions/vehicles/type/tram|7|0|920|1007|580|1684|56170|0.05
None|Total|1038|3|1100|1141|192|4009|4190|7.91

Name|# requests|50%|66%|75%|80%|90%|95%|98%|99%|100%
| ------------- |:-----: |:-----: | :-----:| :-----:| :-----:| :-----:| :-----:| :-----:| :-----:| :-----:|
GET /|33|320|520|790|870|1300|1300|1400|1400|1396
GET /api/v1/emissions/|29|1000|1200|1500|1600|1900|1900|2000|2000|2014
POST /api/v1/emissions/|908|1200|1700|1800|1900|2300|2500|2700|2900|4009
GET /api/v1/emissions/vehicles/1cc2ed4f-4372-4854-b70c-3206c096b6e9|6|880|880|1100|1100|1300|1300|1300|1300|1258
GET /api/v1/emissions/vehicles/46c791af-0ad0-4e65-9941-bbd8f6156acd|13|760|820|1000|1100|1400|1400|1400|1400|1435
GET /api/v1/emissions/vehicles/b25e7f2c-d34e-4c6f-b4cc-c4fdb7ceecd6|10|1300|1300|1500|1500|1600|1600|1600|1600|1589
GET /api/v1/emissions/vehicles/edfde841-177c-4ad9-b640-fbab1404ac79|10|630|1000|1000|1200|1300|1300|1300|1300|1266
GET /api/v1/emissions/vehicles/type/bus|7|760|780|1300|1300|1400|1400|1400|1400|1399
GET /api/v1/emissions/vehicles/type/taxi|5|1500|1600|1600|1600|1600|1600|1600|1600|1646
GET /api/v1/emissions/vehicles/type/train|10|730|820|890|940|1200|1200|1200|1200|1237
GET /api/v1/emissions/vehicles/type/tram|7|920|1000|1100|1100|1700|1700|1700|1700|1684
None Total|1038|1100|1700|1800|1800|2300|2500|2600|2900|4009

## Test 2 <a id="test-2"></a> [^](#toc "To top")  
**Max users concurrently = 250, Spawned users per second = 50**  
Method|Name|# requests|# failures|Median response time|Average response time|Min response time|Max response time|Average Content Size|Requests/s
| ------------- |------------- | :-----:| :-----:| :-----:| :-----:| :-----:| :-----:| :-----:| :-----:|
GET|/|98|0|220|740|192|5577|1313|0.65
GET|/api/v1/emissions/|88|1|680|1159|590|6040|56140|0.59
POST|/api/v1/emissions/|2155|5|540|1983|194|7893|191|14.36
GET|/api/v1/emissions/vehicles/1cc2ed4f-4372-4854-b70c-3206c096b6e9|21|0|630|1086|580|4675|56182|0.14
GET|/api/v1/emissions/vehicles/46c791af-0ad0-4e65-9941-bbd8f6156acd|17|0|680|1011|589|3991|56416|0.11
GET|/api/v1/emissions/vehicles/b25e7f2c-d34e-4c6f-b4cc-c4fdb7ceecd6|24|0|670|979|588|4358|56135|0.16
GET|/api/v1/emissions/vehicles/edfde841-177c-4ad9-b640-fbab1404ac79|10|0|660|1650|614|4511|55901|0.07
GET|/api/v1/emissions/vehicles/type/bus|26|1|870|1679|586|5347|55889|0.17
GET|/api/v1/emissions/vehicles/type/taxi|25|0|690|1117|582|4716|56156|0.17
GET|/api/v1/emissions/vehicles/type/train|14|0|690|1459|587|4752|56417|0.09
GET|/api/v1/emissions/vehicles/type/tram|22|0|670|1211|585|5041|56173|0.15
None|Total|2500|7|620|1859|192|7893|5763|16.66

Name|# requests|50%|66%|75%|80%|90%|95%|98%|99%|100%
| ------------- |:-----: |:-----: | :-----:| :-----:| :-----:| :-----:| :-----:| :-----:| :-----:| :-----:|
GET /|98|220|250|350|590|3500|4000|4100|5600|5577
GET /api/v1/emissions/|88|690|840|990|1000|2900|4500|5800|6000|6040
POST /api/v1/emissions/|2155|540|3200|3900|4100|4800|5500|5800|6000|7893
GET /api/v1/emissions/vehicles/1cc2ed4f-4372-4854-b70c-3206c096b6e9|21|630|660|700|740|1600|4600|4700|4700|4675
GET /api/v1/emissions/vehicles/46c791af-0ad0-4e65-9941-bbd8f6156acd|17|680|960|990|1100|1900|4000|4000|4000|3991
GET /api/v1/emissions/vehicles/b25e7f2c-d34e-4c6f-b4cc-c4fdb7ceecd6|24|690|950|1100|1100|1300|1700|4400|4400|4358
GET /api/v1/emissions/vehicles/edfde841-177c-4ad9-b640-fbab1404ac79|10|670|1200|3200|3700|4500|4500|4500|4500|4511
GET /api/v1/emissions/vehicles/type/bus|26|930|1500|2900|3600|3900|4500|5300|5300|5347
GET /api/v1/emissions/vehicles/type/taxi|25|690|750|790|1100|2800|4600|4700|4700|4716
GET /api/v1/emissions/vehicles/type/train|14|690|1100|1200|3300|4000|4800|4800|4800|4752
GET /api/v1/emissions/vehicles/type/tram|22|680|870|970|1100|3400|3500|5000|5000|5041
None Total|2500|620|3100|3700|4000|4700|5400|5800|5900|7893

## Test 3 <a id="test-3"></a> [^](#toc "To top")  
**Max users concurrently = 500, Spawned users per second = 50**  
Method|Name|# requests|# failures|Median response time|Average response time|Min response time|Max response time|Average Content Size|Requests/s
| ------------- |------------- | :-----:| :-----:| :-----:| :-----:| :-----:| :-----:| :-----:| :-----:|
GET|/|180|0|290|1458|192|8431|1313|1.09
GET|/api/v1/emissions/|168|0|970|2244|596|9157|56155|1.02
POST|/api/v1/emissions/|4382|18|1100|3441|194|14210|191|26.54
GET|/api/v1/emissions/vehicles/1cc2ed4f-4372-4854-b70c-3206c096b6e9|42|0|810|1706|592|8607|56182|0.25
GET|/api/v1/emissions/vehicles/46c791af-0ad0-4e65-9941-bbd8f6156acd|49|0|1100|2278|596|8705|56416|0.30
GET|/api/v1/emissions/vehicles/b25e7f2c-d34e-4c6f-b4cc-c4fdb7ceecd6|57|0|930|1704|585|8813|56135|0.35
GET|/api/v1/emissions/vehicles/edfde841-177c-4ad9-b640-fbab1404ac79|39|0|900|1679|594|7089|55901|0.24
GET|/api/v1/emissions/vehicles/type/bus|35|0|870|2503|601|8690|55884|0.21
GET|/api/v1/emissions/vehicles/type/taxi|37|0|980|1984|589|8256|56150|0.22
GET|/api/v1/emissions/vehicles/type/train|41|0|940|1895|594|9553|56407|0.25
GET|/api/v1/emissions/vehicles/type/tram|45|0|890|2081|585|9571|56172|0.27
None|Total|5075|18|1000|3231|192|14210|5889|30.74

Name|# requests|50%|66%|75%|80%|90%|95%|98%|99%|100%
| ------------- |:-----: |:-----: | :-----:| :-----:| :-----:| :-----:| :-----:| :-----:| :-----:| :-----:|
GET /|180|300|550|990|1200|6000|7600|8000|8400|8431
GET /api/v1/emissions/|168|970|1400|2000|4800|6700|8300|8800|8900|9157
POST /api/v1/emissions/|4382|1100|6100|6800|7400|8200|8700|9000|9100|14210
GET /api/v1/emissions/vehicles/1cc2ed4f-4372-4854-b70c-3206c096b6e9|42|820|970|1200|1600|5900|6400|8600|8600|8607
GET /api/v1/emissions/vehicles/46c791af-0ad0-4e65-9941-bbd8f6156acd|49|1100|1800|2300|5800|6100|6300|8700|8700|8705
GET /api/v1/emissions/vehicles/b25e7f2c-d34e-4c6f-b4cc-c4fdb7ceecd6|57|930|1100|1500|1600|4700|8200|8400|8800|8813
GET /api/v1/emissions/vehicles/edfde841-177c-4ad9-b640-fbab1404ac79|39|900|1100|1300|1700|5800|6900|7100|7100|7089
GET /api/v1/emissions/vehicles/type/bus|35|870|1500|5100|5900|7800|8700|8700|8700|8690
GET /api/v1/emissions/vehicles/type/taxi|37|980|1200|1600|1800|6200|8200|8300|8300|8256
GET /api/v1/emissions/vehicles/type/train|41|940|1300|1500|1700|6000|8000|9600|9600|9553
GET /api/v1/emissions/vehicles/type/tram|45|890|1100|1400|1800|7100|8700|9600|9600|9571
None Total|5075|1000|5800|6600|7200|8100|8600|9000|9100|14210

## Test 4 <a id="test-4"></a> [^](#toc "To top")  
**Max users concurrently = 750, Spawned users per second = 50**  
Method|Name|# requests|# failures|Median response time|Average response time|Min response time|Max response time|Average Content Size|Requests/s
| ------------- |------------- | :-----:| :-----:| :-----:| :-----:| :-----:| :-----:| :-----:| :-----:|
GET|/|239|0|3000|5123|205|17570|1313|1.13
GET|/api/v1/emissions/|248|0|3400|5694|688|18372|56155|1.18
POST|/api/v1/emissions/|6617|24|6300|8678|205|21107|191|31.40
GET|/api/v1/emissions/vehicles/1cc2ed4f-4372-4854-b70c-3206c096b6e9|69|0|3500|5990|766|18335|56183|0.33
GET|/api/v1/emissions/vehicles/46c791af-0ad0-4e65-9941-bbd8f6156acd|72|0|3400|6068|668|17899|56417|0.34
GET|/api/v1/emissions/vehicles/b25e7f2c-d34e-4c6f-b4cc-c4fdb7ceecd6|70|0|3100|4903|723|18473|56136|0.33
GET|/api/v1/emissions/vehicles/edfde841-177c-4ad9-b640-fbab1404ac79|64|0|3000|5959|677|18515|55902|0.30
GET|/api/v1/emissions/vehicles/type/bus|76|0|3300|5233|636|17841|55895|0.36
GET|/api/v1/emissions/vehicles/type/taxi|58|0|4100|6813|749|17855|56155|0.28
GET|/api/v1/emissions/vehicles/type/train|55|0|3700|5961|850|17199|56394|0.26
GET|/api/v1/emissions/vehicles/type/tram|53|0|3500|4542|889|18030|56160|0.25
None|Total|7621|24|4800|8266|205|21107|5843|36.16

Name|# requests|50%|66%|75%|80%|90%|95%|98%|99%|100%
| ------------- |:-----: |:-----: | :-----:| :-----:| :-----:| :-----:| :-----:| :-----:| :-----:| :-----:|
GET /|239|3000|3700|5700|9500|16000|16000|17000|17000|17570
GET /api/v1/emissions/|248|3400|4300|6000|12000|16000|17000|18000|18000|18372
POST /api/v1/emissions/|6617|6300|15000|16000|16000|16000|17000|17000|18000|21107
GET /api/v1/emissions/vehicles/1cc2ed4f-4372-4854-b70c-3206c096b6e9|69|3500|4800|6200|14000|17000|17000|17000|18000|18335
GET /api/v1/emissions/vehicles/46c791af-0ad0-4e65-9941-bbd8f6156acd|72|3400|4600|6900|15000|16000|17000|17000|18000|17899
GET /api/v1/emissions/vehicles/b25e7f2c-d34e-4c6f-b4cc-c4fdb7ceecd6|70|3200|4200|4500|5600|17000|17000|18000|18000|18473
GET /api/v1/emissions/vehicles/edfde841-177c-4ad9-b640-fbab1404ac79|64|3100|4500|6800|15000|17000|17000|18000|19000|18515
GET /api/v1/emissions/vehicles/type/bus|76|3400|4600|5800|6100|17000|17000|17000|18000|17841
GET /api/v1/emissions/vehicles/type/taxi|58|4200|6800|12000|15000|17000|17000|17000|18000|17855
GET /api/v1/emissions/vehicles/type/train|55|3700|5200|6800|14000|16000|17000|17000|17000|17199
GET /api/v1/emissions/vehicles/type/tram|53|3500|4100|4800|5200|6400|17000|17000|18000|18030
None Total|7621|4800|14000|16000|16000|16000|17000|17000|18000|21107

## Test 5 <a id="test-5"></a> [^](#toc "To top")  
**Max users concurrently = 100, Spawned users per second = 50**  
Method|Name|# requests|# failures|Median response time|Average response time|Min response time|Max response time|Average Content Size|Requests/s
| ------------- |------------- | :-----:| :-----:| :-----:| :-----:| :-----:| :-----:| :-----:| :-----:|
GET|/|403|7|4300|6932|200|68788|1313|1.44
GET|/api/v1/emissions/|424|7|17000|26605|786|176413|55913|1.51
POST|/api/v1/emissions/|8515|97|4100|7056|195|96703|191|30.33
GET|/api/v1/emissions/vehicles/431586f0-d19e-45f8-ab1f-784d22899ae7|82|1|14000|23882|819|107692|56063|0.29
GET|/api/v1/emissions/vehicles/b5492d62-61ab-410c-8a0d-d4576f8970ae|101|1|16000|24233|875|123035|55991|0.36
GET|/api/v1/emissions/vehicles/f69760aa-1f63-4d03-a588-552bb04a6813|99|1|19000|27314|1166|123890|55604|0.35
GET|/api/v1/emissions/vehicles/ffc8e318-d7e0-4d0b-ac2b-59d1fe42845c|88|1|14000|21405|800|195564|56005|0.31
GET|/api/v1/emissions/vehicles/type/bus|90|0|16000|22679|941|126426|55891|0.32
GET|/api/v1/emissions/vehicles/type/taxi|102|3|16000|24683|878|112362|56021|0.36
GET|/api/v1/emissions/vehicles/type/train|93|0|15000|24080|2010|91504|56409|0.33
GET|/api/v1/emissions/vehicles/type/tram|75|0|15000|25057|860|108412|55961|0.27
None|Total|10072|118|4300|9117|195|195564|6626|35.87

Name|# requests|50%|66%|75%|80%|90%|95%|98%|99%|100%
| ------------- |:-----: |:-----: | :-----:| :-----:| :-----:| :-----:| :-----:| :-----:| :-----:| :-----:|
GET /|403|4300|5300|7700|9300|17000|23000|28000|33000|68788
GET /api/v1/emissions/|424|17000|27000|37000|42000|58000|78000|96000|112000|176413
POST /api/v1/emissions/|8515|4100|5100|7200|9300|18000|26000|32000|37000|96703
GET /api/v1/emissions/vehicles/431586f0-d19e-45f8-ab1f-784d22899ae7|82|14000|18000|36000|44000|55000|78000|96000|108000|107692
GET /api/v1/emissions/vehicles/b5492d62-61ab-410c-8a0d-d4576f8970ae|101|16000|23000|29000|33000|51000|85000|97000|113000|123035
GET /api/v1/emissions/vehicles/f69760aa-1f63-4d03-a588-552bb04a6813|99|19000|30000|38000|44000|66000|73000|96000|124000|123890
GET /api/v1/emissions/vehicles/ffc8e318-d7e0-4d0b-ac2b-59d1fe42845c|88|14000|19000|25000|32000|44000|56000|117000|196000|195564
GET /api/v1/emissions/vehicles/type/bus|90|16000|20000|27000|31000|52000|81000|101000|126000|126426
GET /api/v1/emissions/vehicles/type/taxi|102|16000|24000|32000|39000|47000|64000|93000|105000|112362
GET /api/v1/emissions/vehicles/type/train|93|15000|21000|32000|44000|61000|72000|91000|92000|91504
GET /api/v1/emissions/vehicles/type/tram|75|15000|26000|33000|42000|60000|88000|101000|108000|108412
None Total|10072|4300|6500|10000|13000|23000|31000|46000|65000|195564
