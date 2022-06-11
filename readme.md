# Geo

Helper scripts for importing and exporting from Notion re: Countries Geographically

## Ext

- [raphaellepuschitz/SVG-World-Map](https://github.com/raphaellepuschitz/SVG-World-Map)

## Usage

Populate your `.SECRET`

```
echo ${NOTION_INTEGRATION_SECRET} > .SECRET
```

Set up venv

```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Execute

```
make learned  # builds learned.svg with map of learned countries
```
