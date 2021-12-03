import hydra
from omegaconf import dictconfig

@hydra.main(config_name="config.yaml", config_path=".")
def main(cfg: dictconfig.DictConfig) ->None:
    print(cfg)

if __name__ == "__main__":
    main()