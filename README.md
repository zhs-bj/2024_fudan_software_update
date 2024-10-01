# Team Fudan 2024 Software Tool

<img src="https://static.igem.wiki/teams/5115/software/software-logo.png" width="80%">

# :tada: Parthub 3.0 :tada:

[Demo](http://47.97.85.37:5000/)

<div style="width: 100%; display: flex; justify-content: center; align-items: center">
<img src="https://badgen.net/badge/platform/Linux,macOS,Windows?list=%7C">
<img src="https://badgen.net/static/Python/3.12/blue">
<img src="https://badgen.net/static/vue/3.4/green">
<img src="https://badgen.net/static/license/CC%20BY%204.0/blue">
<img src="https://badgen.net/docker/size/chc1234567890/fudanigem2024/1.0.0">
</div>
<p style="text-align:center">
  <a href="#dart-about">About</a> &#xa0; | &#xa0; 
  <a href="#sparkles-features">Features</a> &#xa0; | &#xa0;
  <a href="#rocket-technologies">Technologies</a> &#xa0; | &#xa0;
  <a href="#white_check_mark-requirements">Requirements</a> &#xa0; | &#xa0;
  <a href="#checkered_flag-starting">Starting</a> &#xa0; | &#xa0;
  <a href="#memo-license">License</a> &#xa0; | &#xa0;
  <a href="https://github.com/{{YOUR_GITHUB_USERNAME}}" target="_blank">Author</a>
</p>
<br>

## :dart: About

PartHub 3.0 focuses on two critical aspects of parts: **burden estimation** and **similarity query**.

For more information, please visit our [wiki](https://2024.igem.wiki/fudan/software).

## :sparkles: Highlights

:heavy_check_mark: Efficiently uses the iGEM Registry, and supports relevant synthetic biology standards such as Genbank and FASTA format

:heavy_check_mark: Validation against both published and new experimental data

:heavy_check_mark: Flexible and adaptable design, can be easily tailored to a wide range of application scenarios

:heavy_check_mark: Well-documented APIs; easy integration with Snapgene

:heavy_check_mark: Intuitive web UI, comprehensive documentation, and detailed tutorial

## :rocket: Technologies

The following tools were used in this project:

- [Vue.js 3.4](https://vuejs.org/)
- [Ant Design Vue 4.2.3](https://antdv.com/components/overview)
- [Flask](https://flask.palletsprojects.com/en/3.0.x/)
- [Node.js](https://nodejs.org/en/)
- [Docker](https://www.docker.com/)
- [Neo4j 5.11](https://neo4j.com/)

## :checkered_flag: Installation

You can directly visit our **live demo** at http://47.97.85.37:5000/.

#### :white_check_mark: Install with readily available docker image

Please install [Docker](https://www.docker.com/) first, and create a file named `docker-compose.yml` with the following content in your working directory:

```yaml
services:
  flask:
    image: chc1234567890/fudanigem2024:1.0.0
    ports:
      - "5000:5000"
    restart: always
    depends_on:
      - parthub
    environment:
      - SERVER_URL=bolt://parthub:7687
      - SERVER_USER=neo4j
      - SERVER_PASSWORD=igem2024
  parthub:
    image: neo4j:5.11
    restart: always
    environment:
      - NEO4J_AUTH=neo4j/igem2024
      - NEO4J_PLUGINS=["graph-data-science"]
      - NEO4J_dbms_security_procedures_allowlist=gds.*
      - NEO4J_dbms_security_procedures_unrestricted=gds.*
    ports:
      - "7474:7474"
      - "7687:7687"
    deploy:
      resources:
        reservations:
          memory: 2G
```

Then, open the terminal (in Windows, cmd or powershell; in Linux and mac, bash), change the working directory to where `docker-compose.yml` is, and run the following command:

```bash
docker compose up -d
```

Once the deployment is complete, PartHub 3.0 will be running at [http://localhost:5000](http://localhost:5000/).

#### :white_check_mark: Install from source code on Gitlab

The software use [Docker](https://www.docker.com/), [Git](https://git-scm.com) and [Node.js](https://nodejs.org/en) for deployment, so please install them first!

For Linux and mac platform, run the following commands in bash:

```bash
git clone https://gitlab.igem.org/2024/software-tools/fudan.git
cd fudan/webUI
npm install
cd ..
bash pack.sh
```

For Windows platform, run the following commands in cmd or powershell:

```bat
git clone https://gitlab.igem.org/2024/software-tools/fudan.git
cd fudan/webUI
npm install
cd ..
pack.bat
```

Once the deployment is complete, PartHub 3.0 will be running at [http://localhost:5000](http://localhost:5000/).

## :memo: License

This project is under license of Creative Commons Attribution 4.0 International. For more details, see the [LICENSE](https://gitlab.igem.org/2024/software-tools/fudan/-/blob/main/LICENSE) file.

## :shake: Acknowledgments

We would like to thank the previous Fudan iGEM team members for their contributions to the development of PartHub 1.0 and 2.0.

<br>

Developed by Hongcheng Chen ([@chc1234567890](https://github.com/chc1234567890))

<br>

<a href="#top">Back to top</a>
