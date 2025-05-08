# 使用 CentOS 7 作为基础镜像
FROM centos:7

# 设置工作目录为 /code
WORKDIR /code

# 安装必要的软件包，包括 Python 3.6 和文泉驿字体
RUN yum install epel-release python36 fontconfig wqy-microhei-fonts -y

# 安装 Python 的 ensurepip 模块
RUN python3.6 -m ensurepip --default-pip

# 升级 pip
RUN pip3.6 install pip --upgrade

# 安装 nmap 工具
RUN yum install nmap -y

# 安装 Python 开发工具和 GCC 编译器
RUN yum install python36-devel gcc-c++ -y

# 安装 nginx、unzip 和 wget
RUN yum install nginx unzip wget -y

# 复制应用程序代码到容器中
COPY app/ app/

# 复制测试代码到容器中
COPY test/ test/

# 创建 phantomjs 的符号链接
RUN ln -s /code/app/tools/phantomjs /usr/bin/phantomjs

# 复制前端代码到容器中
COPY docker/frontend/ frontend/

# 复制 nginx 配置文件到容器中
COPY docker/nginx.conf /etc/nginx/nginx.conf

# 复制生成 SSL 证书的脚本到容器中
COPY docker/worker/gen_crt.sh /usr/bin/gen_crt.sh

# 复制 wait-for-it 脚本到容器中
COPY docker/worker/wait-for-it.sh /usr/bin/wait-for-it.sh

# 复制 ncrack 工具及其依赖到容器中
COPY docker/ncrack /usr/local/bin/ncrack
COPY docker/ncrack-services /usr/local/share/ncrack/ncrack-services

# 复制 NPoC 工具到容器中并安装
COPY docker/NPoC/ /opt/NPoC/
WORKDIR /opt/NPoC/
# 设置语言环境为 UTF-8
ENV LANG en_US.UTF-8
# 安装 NPoC 的 Python 依赖
RUN pip3.6 install -e .

# 切换回工作目录 /code
WORKDIR /code

# 下载 Mozilla 提供的 SSL 配置文件
RUN curl https://ssl-config.mozilla.org/ffdhe2048.txt -o /etc/ssl/certs/dhparam.pem

# 复制 Python 的依赖文件 requirements.txt
COPY requirements.txt requirements.txt

# 设置 pip 的镜像源反向代理地址
RUN pip3.6 config set global.index-url https://mirrors.tsaitang.com/language/pypi

# 复制 GeoLite2 数据到容器中
COPY docker/GeoLite2/ /data/GeoLite2/

# 安装 Python 的依赖包
RUN pip3.6 install -r requirements.txt

# 安装 NPoC 的依赖包
WORKDIR /opt/NPoC/
RUN pip3.6 install -r requirements.txt

# 定义 nuclei 的版本号
ARG NUCLEI_VERSION=3.2.4

# 下载并安装 nuclei 工具
RUN wget -c "https://github.com/tsaitang404/CASM/raw/master/tools/nuclei.zip" \
    && unzip "nuclei.zip" nuclei \
    && mv nuclei /usr/bin/ \
    && rm -f "nuclei.zip"

# 更新 nuclei 的模板
RUN nuclei -ut

# 下载并安装 WIH 工具
RUN wget -c https://github.com/tsaitang404/CASM/raw/master/tools/wih/wih_linux_amd64 -O /usr/bin/wih && chmod +x /usr/bin/wih
# 验证 WIH 工具的版本
RUN wih --version

# 切换工作目录为 /code
WORKDIR /code

# 复制配置文件示例并进行自测
RUN cp app/config.yaml.example app/config.yaml
RUN env FLASK_APP=app.main:casm_app python3.6 -m flask routes
RUN python3 -m app.celerytask
