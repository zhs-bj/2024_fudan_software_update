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

PartHub 3.0 focuses on two critical aspects of parts: **burden prediction** and **similarity estimation**.

For more information, please visit our [wiki](https://2024.igem.wiki/fudan/software).

## :sparkles: Highlights

:heavy_check_mark: Efficiently uses the iGEM Registry, and supports relevant synthetic biology standards such as Genbank and FASTA format

:heavy_check_mark: Validation against both published and new experimental data

:heavy_check_mark: Flexible and adaptable design, can be easily tailored to a wide range of application scenarios

:heavy_check_mark: Well-documented APIs; easy integration with Snapgene

:heavy_check_mark: Intuitive web UI and detailed tutorial

## :rocket: Technologies

The following technologies were used in this project:

- [Vue.js 3.4](https://vuejs.org/)
- [Ant Design Vue 4.2.3](https://antdv.com/components/overview)
- [Flask](https://flask.palletsprojects.com/en/3.0.x/)
- [Node.js](https://nodejs.org/en/)
- [Docker](https://www.docker.com/)
- [Neo4j 5.11](https://neo4j.com/)

## :checkered_flag: Installation

You can directly visit our **live demo** at http://47.97.85.37:5000/.

**Note:** When deploying this software, an internet connection is required to download and install BLAST, gcc, and g++ in the docker container.

### :white_check_mark: Install with readily available docker image

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

### :white_check_mark: Install from source code on Gitlab

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

## Acknowledgments

We would like to thank the previous Fudan iGEM team members for their contributions to the development of PartHub 1.0 and 2.0.

<br>

Developed by Hongcheng Chen ([@chc1234567890](https://github.com/chc1234567890))

<br>

<a href="#top">Back to top</a>

## 更新日志

### 2026-05-10

本次更新围绕**搜索功能重构**、**Docker 部署优化**和**代码质量提升**三个方向展开，具体改动如下。

---

#### 1. 修复 Content 字段搜索 Bug（`parthub/utils.py`）

**问题描述**

原代码使用 `re.sub('type', search_type, query)` 进行占位符替换，意图将模板字符串中的 `type` 替换为实际搜索字段名。但当 `search_type` 为 `contents` 时，正则模式 `type` 会错误地匹配到 `contents` 内部的子串 `type`，导致字段名被篡改为不存在的 `concontents`，查询永远返回空。

**修复方式**

去掉两层 `re.sub` 的迂回替换，改用 f-string 直接拼接，并对 `search_key` 使用 `re.escape` 防止注入：

```python
# 修复前（错误）
query = f"_.{search_type} =~ '(?i).*key.*'"
query_temp = re.sub('type', search_type, query)
query = re.sub('key', search_key, query_temp)

# 修复后（正确）
query = f"_.{search_type} =~ '(?i).*{re.escape(search_key)}.*'"
```

**影响范围**

- 修复前：选择 **Content** 搜索类型时，无论输入什么关键词都返回 `No search result found`。
- 修复后：**Content** 搜索恢复正常，可正确匹配零件描述中的关键词。

---

#### 2. 新增全文索引模糊搜索（`parthub/utils.py` + `init_fulltext_index.py`）

**功能说明**

引入 Neo4j 原生 **Lucene 全文索引**（`partSearch`），覆盖字段 `number`、`name`、`contents`、`designer`、`team`。搜索时自动优先走全文索引，支持以下能力：

- **拼写容错**：输入 `promotr`（少一个字母）也能匹配 `promoter`（Lucene `~` 模糊查询）。
- **多词组合搜索**：输入多个关键词时自动转换为 `field:word1~ AND field:word2~` 的 Lucene 语法。
- **相关性排序**：返回结果自带 Lucene 相关性分数 `_score`，排序时与 PageRank 加权结合，优先展示高质量结果。

**前后对比**

| 场景 | 修复前（子串匹配） | 修复后（全文索引） |
|------|-------------------|-------------------|
| 拼写错误 `promotr` | 返回空 | 返回 `promoter` 相关结果 |
| 多词搜索 `T7 promoter` | 必须连续完整出现 | 支持分词组合匹配 |
| 大小写 | 不敏感（已有） | 不敏感（Lucene 标准分析器） |
| 排序依据 | 仅 PageRank | PageRank × Lucene 相关性加权 |

**新增文件**

- `parthub/init_fulltext_index.py`：独立脚本，支持 `create` / `drop` 操作，用于管理全文索引的创建与删除。容器启动时由 `flask-compose.sh` 自动调用。

---

#### 3. 新增序列搜索 BLAST 降级策略（`parthub/utils.py`）

**功能说明**

针对 **Sequence** 搜索类型，增加两级 fallback：

1. **精确匹配**：先搜索包含目标序列（含反向互补）的零件。
2. **BLAST 模糊比对**：若精确匹配无结果，自动调用本地 `blastn-short`（短序列）或 `blastn`（长序列）对全库进行比对，容忍碱基错配、缺失等差异。

**适用场景**

- 用户输入的序列与数据库记录存在少量碱基差异（如测序误差、突变体）。
- 输入的序列较短（≤32 bp），常规精确匹配过于严格。

**前后对比**

| 场景 | 修复前 | 修复后 |
|------|--------|--------|
| 精确匹配失败 | 直接返回空 | 自动启动 BLAST 模糊比对 |
| 短序列（≤32 bp） | 无特殊处理 | 使用 `blastn-short` 优化 |

---

#### 4. 重构搜索结果排序逻辑（`parthub/utils.py`）

**改动内容**

- 提取公共节点处理逻辑到 `_process_node_records`，统一处理全文索引结果和 legacy 结果。
- 排序时引入 **组合分数**：`combined_score = lucene_score × (1 + normalized_pagerank × 2)`，兼顾相关性和图结构重要性。
- `content_match` 不再依赖 `search_key` 做上下文截取，改为统一返回前 40 个词的内容摘要，简化逻辑并避免截断错误。

---

#### 5. 优化 Docker 部署流程

##### 5.1 `Dockerfile`

- **国内镜像加速**：基础镜像从 `python:3.10-slim` 改为 `docker.m.daocloud.io/library/python:3.10-slim`，解决国内网络拉取 Docker Hub 镜像超时的问题。
- **移除 BLAST 本地依赖**：不再 `COPY blast.tar.gz`，改为在容器启动时通过 `wget` 动态下载，减小镜像体积，避免构建时本地文件缺失导致失败。
- **新增文件 COPY**：补充 `parthub/init_fulltext_index.py`，确保容器内具备全文索引管理能力。

##### 5.2 `flask-compose.sh`

- **修正 BLAST 下载 URL**：从 `blast+/LATEST/...` 改为固定版本 `blast+/2.16.0/...`，避免上游更新导致链接失效。
- **优化解压逻辑**：将 `tar -zxvf` 和 `mv` 操作从循环外移到下载逻辑内，避免每次重试都重复解压。
- **新增全文索引自动创建**：在 `upload_collections.py` 成功导入数据后，自动执行 `python parthub/init_fulltext_index.py create`，确保容器重启后索引不丢失。

##### 5.3 `parthub/upload_collections.py`

- **移除 GDS 图算法初始化**：删除 PageRank、Louvain 社区检测和 `gds.graph.project` 相关代码。
- **原因**：Neo4j 的 GDS 插件在 Docker 部署中需要额外配置且容易版本不兼容；简化后仅依赖 Neo4j 核心功能，启动更稳定。
- **数据层面**：节点属性 `pagerank`、`community`、`nodesize` 改为在导入时直接写入固定默认值（`pagerank=0.15, community=0, nodesize=30`），保证前端渲染不报错，后续可独立运行 GDS 计算更新。

**前后对比**

| 项目 | 修复前 | 修复后 |
|------|--------|--------|
| 镜像拉取 | 经常超时失败 | 使用 DaoCloud 国内源，稳定 |
| BLAST 下载 | 链接指向 LATEST，易失效 | 固定 2.16.0 版本，可靠 |
| 容器启动 | 需手动创建全文索引 | 启动时自动创建 |
| GDS 依赖 | 必须安装 GDS 插件 | 零插件依赖，启动更简单 |

---

#### 6. 其他改进

- **前端搜索类型默认值**：`parthub.vue` 中 `searchType` 默认仍为 `id`（实际对应 `number` 字段），用户搜索时需注意切换为 **Name** 或 **Content** 以获得最佳体验。
- **代码结构**：`utils.py` 按功能模块拆分为 Lucene 查询 helpers、全文搜索、Legacy 搜索、序列搜索、排序等独立区块，提升可维护性。
