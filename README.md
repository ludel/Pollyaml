# Pollyaml

Create a poll quickly and easily with the power of the YAML markup language.

[Website](https://pollyaml.com/)

![capture.jpg](https://raw.githubusercontent.com/ludel/pollyaml/master/screenshot-index.jpg)
___
![capture.jpg](https://raw.githubusercontent.com/ludel/pollyaml/master/screenshot-poll.jpg)

## Tech Stack

- Backend: [Bottle](https://bottlepy.org/docs/dev/)
- Frontend: [Sceptre-css](https://picturepan2.github.io/spectre/)
- Data: [Yaml](https://fr.wikipedia.org/wiki/YAML)

## Docker

You can build a docker image. The server is by default in production environment and runs with gunicorn. 

```bash
> docker build . -t pollyaml
> docker run -p 8000:8000 pollyaml
```

## License

Pollyaml is MIT licensed.

