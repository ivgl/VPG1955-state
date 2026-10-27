> **ВАЖНО: переход на приватный GitHub.** ТЕКУЩАЯ СВЕРКА 27.10.2026 (архив до RC1.0). **После редакции RC1.0 регистрация открыта, но фаза PREPARE сохраняется**. Единственная каноническая фаза — `ivgl/VPG1955-state@main:HEAD.json`: `campaign_id=VPI1955_MAIN`, `year=1955`, `phase=PREPARE`, `rules_version=RC0.8`, `manifest_sha256=b43c6e254fcdf2a1b8ac8b9ca1c2b46e647a3197e9068d4c72d769122698bfdb`. Приём не открыт. Текст ниже — **исторический статус Drive-импорта**; `official_head_id` в Drive и `d310f7...` НЕ являются актуальными. Этот документ нельзя использовать как независимо обновляемый статус; текущий HEAD читать при каждом запуске чата. См. `STATE_WORKFLOW.md`, `docs/TRANSFER_AUDIT_2026-10-27.md`. 

---

# ВПИ 1955 — статус первого игрового хода

Новый статус не наследует результаты операций 1976/1977 и не принимает их за мир 1955\.

schema: vpi-turn-status-1955-rp-1 ; campaign\_id: VPI1955\_MAIN ; turn\_year:1955 ; world\_date\_at\_start: 1955-01-01 ; phase:PREPARE ; source\_release:VPI1955-1955-START-R1 ; official\_head\_id: 1npjztHH-CLG772KqY\_t6VuKeMO8YSkts ; manifest\_sha256: d310f7d9006b6cfb9141e63619ff1a9919ee4930ecec107be82cc51e825bfa7d.

required\_country\_ids: USA, SUN, GBR, FRA, DEU, JPN, CHN, EGY, IND, ISR, ITA, YUG

post\_count: 0 ; locked\_submissions: \[\] ; approved\_decisions: \[\] ; published\_verdicts: \[\] ; open\_appeals: \[\] ; already\_applied\_effect\_ids: \[\] ; commit\_id: null.

HEAD и проверенный SHA-манифест 1955 опубликованы. Окно подачи постов остаётся закрыто на стадии PREPARE до отдельной команды администратора открыть приём, объявить сроки и публикуемую вводную.

Состояния: PREPARE → RECEIVING → LOCKED → IN\_REVIEW → ADMIN\_APPROVED → VERDICTS\_PUBLISHED → APPEALS\_OPEN → APPEALS\_REVIEW → FINAL\_APPROVED → COMMITTED → NEXT\_PREPARE.

Переходы допускает администратор. Простой черновик вердикта не меняет статистику. Для внешней сделки требуется подтверждение контрагента, для бюджета — источник финансирования, для повышения боеспособности — существующие люди, материальные ресурсы и время.

После завершения 1955 должны появиться неизменяемый snapshot 1956, manifest, проверенные 12 Google Sheets с новым листом «1956» и TURN\_HANDOFF; переключение нового официального HEAD — последним.

Операционная папка: https\://drive.google.com/drive/folders/1m\_Q9HePBbLASsass\_7My\_ieSbXKLScZP  
