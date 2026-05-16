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

#### 1. 新增全文索引模糊搜索（`parthub/utils.py` + `init_fulltext_index.py`）

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

### 2026-05-16

本次更新新增**语义搜索（Semantic Search / Feature Search）**功能，用户可通过自然语言描述零件功能进行智能检索，无需记忆精确名称或关键词。

---

#### 1. 新增语义搜索功能

**功能说明**

在原有 ID / Name / Sequence / Designer / Team / Content 六种搜索类型的基础上，新增 **Feature** 搜索模式。用户输入自然语言描述（如 *"protein that glows green"*、*"promoter activated by arabinose"*），系统通过语义向量相似度返回最相关的零件。

**技术实现**

- **Embedding 模型**：采用 `sentence-transformers/all-MiniLM-L6-v2`（384 维，开源轻量）。
- **离线索引**：`parthub/build_semantic_index.py` 遍历所有 Part 节点，将 `name + contents` 预编码为 embedding 矩阵，持久化到 `parthub/semantic_data/`。
- **在线检索**：用户查询实时编码为向量，通过归一化余弦相似度与全库预计算向量比对，返回 Top-K 最相似零件。
- **排序依据**：纯语义相似度得分 `_score`（范围 0~1），结果页以 **Similarity: xx.x%** 标签展示。

**新增文件**

- `parthub/semantic_search.py`：核心语义搜索模块，含模型懒加载、embedding 计算、相似度检索、Neo4j 节点召回。
- `parthub/build_semantic_index.py`：离线构建脚本，首次部署或数据更新后运行一次即可。

**前后对比**

| 场景 | 修复前（关键词搜索） | 修复后（语义搜索） |
|------|-------------------|-------------------|
| 描述性查询 `protein that glows green` | 无精确关键词，返回空 | 理解语义，返回 GFP 等荧光蛋白 |
| 同义表达 `antibiotic resistance for kanamycin` | 必须匹配字段文本 | 向量相似度匹配，容忍同义改写 |
| 功能导向搜索 `high copy plasmid backbone` | 依赖内容中出现完整词组 | 语义层面匹配质粒骨架相关描述 |

---

#### 2. 新增语义搜索 API（`app.py`）

- **路由**：`POST /api/parthub/semantic_search`
- **请求体**：`{"query": "描述文本", "top_k": 50}`
- **响应**：零件 JSON 数组，含 `_score` 相似度字段；若索引未生成返回 503 提示。

---

#### 3. 前端适配语义搜索

- **`webUI/src/views/parthub/parthub.vue`**：搜索类型增加 **Feature** 单选按钮；选择后输入框 placeholder 动态提示用户输入自然语言描述。
- **`webUI/src/views/parts/parts.vue`**：根据 `localStorage` 中的 `partHubSearchMode` 自动路由到语义搜索 API 或原有关键词搜索 API；结果页保留 Feature 选项，支持在结果页直接切换搜索模式。
- **`webUI/src/components/partcard.vue`**：语义搜索模式下显示橙色 **Similarity** 标签，并关闭关键词红色高亮（避免自然语言查询词无意义高亮）。

---

#### 4. Docker 部署增强

##### 4.1 `Dockerfile`

- 新增 COPY 指令，将 `parthub/semantic_search.py` 和 `parthub/build_semantic_index.py` 打包进容器，确保语义搜索模块可用。

##### 4.2 `docker-compose.yml`

- **数据持久化**：Neo4j 服务新增 bind mount，将容器内 `/data` 映射到宿主机 `D:\Neo4jData\parthub`，避免数据存储在 Docker 虚拟磁盘中，方便用户直接管理磁盘空间。

##### 4.3 `flask-compose.sh`

- **自动构建语义索引**：在数据导入、全文索引创建、BLAST 数据库构建完成后，自动执行 `python parthub/build_semantic_index.py`，下载模型并生成 embedding，实现"一键启动，全功能可用"。

**部署命令**

```bash
docker-compose up --build -d
```

启动后访问 [http://localhost:5000/parthub](http://localhost:5000/parthub)，选择 **Feature** 即可体验语义搜索。

---

#### 5. 依赖更新

- `requirements.txt`：新增 `torch==2.12.0` 和 `sentence-transformers==5.5.0`。

---

#### 6. 其他改进

- **`parthub/semantic_search.py`** 中 Neo4j 连接采用懒加载模式，避免模块导入时即尝试连接数据库，提升启动稳定性。
