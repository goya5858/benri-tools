import hydra
from omegaconf import dictconfig

@hydra.main(config_name="config.yaml", config_path=".")
def main(cfg: dictconfig.DictConfig) ->None:
    print(cfg.model.node1)
    print(cfg.optimizer.lr)

if __name__ == "__main__":
    main()