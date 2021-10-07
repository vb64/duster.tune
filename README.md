# Пути для ELM327

В выпадающем списке: XJD - DUSTER II

## Часы на приборной панели.

- Cluster/TDB -> Cluster_L1_L2_v6.09
- [Cluster/TDB] Cluster_L1_L2_v6.09
- Ercans Configuration -> Conf_2 Prestations IHM

Clock_CF ‐> Clock displayed and set/RTC ON 

ExpertMode, Clock, setSW


## Настройка режима ECO.

Режим ECO включается при запуске двигателя, если он был включен перед тем, как заглушили двигатель (запоминает состояние). 

- BCM/UCH -> T4_VS_BCM_BIS_DOT2000_SW13_1
- [BCM/UCH] T4_VS_BCM_BIS_DOT2000_SW13_1
- Fal MMI -> Fal MMI - Configuration

ECOMODE_PREVIOUS_RESTART_CF -> true

ExpertMode, set
