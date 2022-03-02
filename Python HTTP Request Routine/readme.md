# Python HTTP Request Routine

<i>This routine can run on os that support python like raspberry pi, etc</i>

## API Reference

#### Send Hardware Sensor Data

```http
  POST /addhardwarelog
```

| Parameter       | Type     | Description                      |
| :-------------- | :------- | :------------------------------- |
| `id_hardware`   | `int`    | **Required**. Get from dashboard |
| `security_code` | `string` | **Required**. Set from dashboard |
| `ph_level`      | `int`    | **Required**.                    |
| `temperature`   | `int`    | **Required**.                    |
| `humidity`      | `int`    | **Required**.                    |
| `water_level`   | `int`    | **Required**.                    |
| `image`         | `blob`   | **Required**.                    |

#### Get hardware status

```http
  GET /checkhardwarestatus/${id_hardware}
```

| Parameter     | Type  | Description                           |
| :------------ | :---- | :------------------------------------ |
| `id_hardware` | `int` | **Required**. Id of hardware to fetch |
