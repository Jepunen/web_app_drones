# web_app_drones

Drone info format (XML)
```
<report>
  <deviceInformation deviceId="GUARDB1RD">
    <listenRange>500000</listenRange>
    <deviceStarted>2022-12-16T00:51:58.437Z</deviceStarted>
    <uptimeSeconds>51817</uptimeSeconds>
    <updateIntervalMs>2000</updateIntervalMs>
  </deviceInformation>
  <capture snapshotTimestamp="2022-12-16T15:15:35.303Z">
    <drone>
      <serialNumber>SN-065rnhjZEh</serialNumber>
      <model>Altitude X</model>
      <manufacturer>DroneGoat Inc</manufacturer>
      <mac>81:3f:8a:9d:e2:9e</mac>
      <ipv4>45.217.40.162</ipv4>
      <ipv6>8829:be40:5fa0:d533:dc75:4b8a:de2d:a8b9</ipv6>
      <firmware>5.1.3</firmware>
      <positionY>499579.7918217554</positionY>
      <positionX>269199.0140938187</positionX>
      <altitude>4482.699379602072</altitude>
    </drone>
    <drone>
      <serialNumber>SN-aRLKgq2DFH</serialNumber>
      <model>Falcon</model>
      <manufacturer>MegaBuzzer Corp</manufacturer>
      <mac>32:4c:9c:3b:e6:85</mac>
      <ipv4>205.52.31.27</ipv4>
      <ipv6>b6dc:e99e:684c:3537:8463:4306:1ae2:0a8c</ipv6>
      <firmware>7.7.1</firmware>
      <positionY>416561.7846361406</positionY>
      <positionX>176647.78723101385</positionX>
      <altitude>4776.992690708621</altitude>
    </drone>
    <drone>
      <serialNumber>SN-F50trmtEgX</serialNumber>
      <model>Mosquito</model>
      <manufacturer>MegaBuzzer Corp</manufacturer>
      <mac>86:e1:63:a5:43:a5</mac>
      <ipv4>19.177.156.246</ipv4>
      <ipv6>66e8:636a:eb6d:334d:ab83:1427:8c0d:861a</ipv6>
      <firmware>4.7.9</firmware>
      <positionY>377842.6719721566</positionY>
      <positionX>215963.3899583773</positionX>
      <altitude>4764.7797459250505</altitude>
    </drone>
  </capture>
</report>
```
Pilot info format (JSON)
```
{
  "pilotId":"P-dkTvj_vKQQ",
  "firstName":"Lionel",
  "lastName":"Denesik",
  "phoneNumber":"+210716097586",
  "createdDt":"2022-09-10T12:31:41.457Z",
  "email":"lionel.denesik@example.com"
}
```
