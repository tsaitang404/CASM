set -e
# 配置源
cd /etc/yum.repos.d/
sed -i 's/mirrorlist/#mirrorlist/g' /etc/yum.repos.d/CentOS-*
sed -i 's|baseurl=http://.*centos.org|baseurl=https://mirrors.tsaitang.com/system/centos|g' /etc/yum.repos.d/CentOS-*
sed -i 's|#baseurl=https://mirrors.tsaitang.com/system/centos|baseurl=https://mirrors.tsaitang.com/system/centos|g' /etc/yum.repos.d/CentOS-*

echo "cd /opt/"

mkdir -p /opt/
cd /opt/

# 配置dns服务器
tee /etc/resolv.conf <<"EOF"
nameserver 180.76.76.76
nameserver 4.2.2.1
nameserver 1.1.1.1
EOF

# 添加mongodb源
tee /etc/yum.repos.d/mongodb-org-4.0.repo <<"EOF"
[mongodb-org-4.0]
name=MongoDB Repository
baseurl=https://repo.mongodb.org/yum/redhat/$releasever/mongodb-org/4.0/x86_64/
gpgcheck=1
enabled=1
gpgkey=https://www.mongodb.org/static/pgp/server-4.0.asc
EOF

# 添加rabbitmq源
tee //etc/yum.repos.d/rabbitmq.repo <<"EOF"
[rabbitmq_erlang]
name=rabbitmq_erlang
baseurl=https://packagecloud.io/rabbitmq/erlang/el/8/$basearch
repo_gpgcheck=1
gpgcheck=1
enabled=1
# PackageCloud's repository key and RabbitMQ package signing key
gpgkey=https://packagecloud.io/rabbitmq/erlang/gpgkey
       https://github.com/rabbitmq/signing-keys/releases/download/2.0/rabbitmq-release-signing-key.asc
sslverify=1
sslcacert=/etc/pki/tls/certs/ca-bundle.crt
metadata_expire=300

[rabbitmq_erlang-source]
name=rabbitmq_erlang-source
baseurl=https://packagecloud.io/rabbitmq/erlang/el/8/SRPMS
repo_gpgcheck=1
gpgcheck=0
enabled=1
gpgkey=https://packagecloud.io/rabbitmq/erlang/gpgkey
       https://github.com/rabbitmq/signing-keys/releases/download/2.0/rabbitmq-release-signing-key.asc
sslverify=1
sslcacert=/etc/pki/tls/certs/ca-bundle.crt
metadata_expire=300

[rabbitmq_server]
name=rabbitmq_server
baseurl=https://packagecloud.io/rabbitmq/rabbitmq-server/el/8/$basearch
repo_gpgcheck=1
gpgcheck=0
enabled=1
gpgkey=https://packagecloud.io/rabbitmq/rabbitmq-server/gpgkey
       https://github.com/rabbitmq/signing-keys/releases/download/2.0/rabbitmq-release-signing-key.asc
sslverify=1
sslcacert=/etc/pki/tls/certs/ca-bundle.crt
metadata_expire=300

[rabbitmq_server-source]
name=rabbitmq_server-source
baseurl=https://packagecloud.io/rabbitmq/rabbitmq-server/el/8/SRPMS
repo_gpgcheck=1
gpgcheck=0
enabled=1
gpgkey=https://packagecloud.io/rabbitmq/rabbitmq-server/gpgkey
sslverify=1
sslcacert=/etc/pki/tls/certs/ca-bundle.crt
metadata_expire=300
EOF

echo "install dependencies ..."
cd /opt/
# 安装依赖
yum update -y
yum install epel-release -y
yum install systemd -y
yum install rabbitmq-server --nobest -y
yum install python36 mongodb-org-server mongodb-org-shell python36-devel gcc-c++ git nginx fontconfig wqy-microhei-fonts unzip wget -y

# 安装链接python3.6
if [ ! -f /usr/bin/python3.6 ]; then
  echo "link python3.6"
  ln -s /usr/bin/python36 /usr/bin/python3.6
fi

# 安装python3.6 pip
if [ ! -f /usr/local/bin/pip3.6 ]; then
  echo "install  pip3.6"
  python3.6 -m ensurepip --default-pip
  python3.6 -m pip install --upgrade pip
  pip3.6 config --global set global.index-url https://mirrors.tsaitang.com/language/pypi
  pip3.6 --version
fi

# 安装 nmap
if ! command -v nmap &> /dev/null
then
    echo "install nmap ..."
    yum install nmap -y
fi

# 安装 nuclei
if ! command -v nuclei &> /dev/null
then
  echo "install nuclei"
  wget -c https://github.com/tsaitang404/CASM/raw/master/tools/nuclei.zip -O nuclei.zip
  unzip nuclei.zip && mv nuclei /usr/bin/ && rm -f nuclei.zip
  nuclei -ut
  rm -rf /opt/*
fi

# 安装wih
if ! command -v wih &> /dev/null
then
  echo "install wih ..."
  ## 安装 WIH
  wget -c https://github.com/tsaitang404/CASM/raw/master/tools/wih/wih_linux_amd64 -O /usr/bin/wih && chmod +x /usr/bin/wih
  wih --version
fi

# 启动系统组件
echo "start services ..."
systemctl enable mongod
systemctl restart mongod
systemctl enable rabbitmq-server
systemctl restart rabbitmq-server

# 克隆CASM
cd /opt
if [ ! -d CASM ]; then
  echo "git clone CASM proj"
  git clone https://github.com/tsaitang404/CASM
fi

if [ ! -d "NPoC" ]; then
  echo "mv NPoC proj"
 mv CASM/tools/NPoC NPoC
fi

# 安装NPoC依赖
cd /opt/NPoC
echo "install poc requirements ..."
pip3.6 install -r requirements.txt
pip3.6 install -e .
cd ../

if [ ! -f /usr/local/bin/ncrack ]; then
  echo "Download ncrack ..."
  wget -c https://github.com/tsaitang404/CASM/raw/master/tools/ncrack -O /usr/local/bin/ncrack
  chmod +x /usr/local/bin/ncrack
fi

mkdir -p /usr/local/share/ncrack
if [ ! -f /usr/local/share/ncrack/ncrack-services ]; then
  echo "Download ncrack-services ..."
  wget -c https://github.com/tsaitang404/CASM/raw/master/tools/ncrack-services -O /usr/local/share/ncrack/ncrack-services
fi

mkdir -p /data/GeoLite2
if [ ! -f /data/GeoLite2/GeoLite2-ASN.mmdb ]; then
  echo "download GeoLite2-ASN.mmdb ..."
  wget -c https://github.com/tsaitang404/CASM/raw/master/tools/GeoLite2-ASN.mmdb -O /data/GeoLite2/GeoLite2-ASN.mmdb
fi

if [ ! -f /data/GeoLite2/GeoLite2-City.mmdb ]; then
  echo "download GeoLite2-City.mmdb ..."
  wget -c https://github.com/tsaitang404/CASM/raw/master/tools/GeoLite2-City.mmdb -O /data/GeoLite2/GeoLite2-City.mmdb
fi

cd /opt/CASM
# 初始化mq、mongo
if [ ! -f rabbitmq_user ]; then
  echo "add rabbitmq user"
  rabbitmqctl add_user casm casmpassword
  rabbitmqctl add_vhost casmv2host
  rabbitmqctl set_user_tags casm casmtag
  rabbitmqctl set_permissions -p casmv2host casm ".*" ".*" ".*"
  echo "init casm user"
  mongo 127.0.0.1:27017/casm docker/mongo-init.js
  touch rabbitmq_user
fi

# 安装CASM依赖
echo "install casm requirements ..."
pip3.6 install -r requirements.txt
if [ ! -f app/config.yaml ]; then
  echo "create config.yaml"
  cp app/config.yaml.example  app/config.yaml
fi

if [ ! -f /usr/bin/phantomjs ]; then
  echo "install phantomjs"
  ln -s `pwd`/app/tools/phantomjs  /usr/bin/phantomjs
fi

if [ ! -f /etc/nginx/conf.d/casm.conf ]; then
  echo "copy casm.conf"
  cp misc/casm.conf /etc/nginx/conf.d
fi



if [ ! -f /etc/ssl/certs/dhparam.pem ]; then
  echo "download dhparam.pem"
  curl https://ssl-config.mozilla.org/ffdhe2048.txt > /etc/ssl/certs/dhparam.pem
fi


echo "gen cert ..."
chmod +x docker/worker/gen_crt.sh
./docker/worker/gen_crt.sh


cd /opt/CASM/


if [ ! -f /etc/systemd/system/casm-web.service ]; then
  echo  "copy casm-web.service"
  cp misc/casm-web.service /etc/systemd/system/
fi

if [ ! -f /etc/systemd/system/casm-worker.service ]; then
  echo  "copy casm-worker.service"
  cp misc/casm-worker.service /etc/systemd/system/
fi


if [ ! -f /etc/systemd/system/casm-worker-github.service ]; then
  echo  "copy casm-worker-github.service"
  cp misc/casm-worker-github.service /etc/systemd/system/
fi

if [ ! -f /etc/systemd/system/casm-scheduler.service ]; then
  echo  "copy casm-scheduler.service"
  cp misc/casm-scheduler.service /etc/systemd/system/
fi

chmod +x /opt/CASM/app/tools/*

echo "start casm services ..."

systemctl enable casm-web
systemctl restart casm-web
systemctl enable casm-worker
systemctl restart casm-worker
systemctl enable casm-worker-github
systemctl restart casm-worker-github
systemctl enable casm-scheduler
systemctl restart casm-scheduler
systemctl enable nginx
systemctl restart nginx

python3.6 tools/add_finger.py
python3.6 tools/add_finger_ehole.py

echo "install done"
