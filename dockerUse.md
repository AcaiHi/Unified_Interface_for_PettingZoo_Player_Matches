## 編譯
```bash
docker build -t my-cuda-env .
```

## 執行 (執行在 8888 port & use gpu)
```bash
docker run -it --gpus all -p 8888:8888 my-cuda-env
```

## 後臺執行
```bash
docker run -it --gpus all -p 8888:8888 -d my-cuda-env
```

## 刪除服務
```bash
docker ps # 查看 container id
docker stop <container_id> # 停止 container
docker rm <container_id> # 刪除 container
```