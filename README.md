# 笑傲江湖人物關係網路

## INSTALL

1. `cd Social-Network-of-Martial-arts-and-chivalry-novels-`
2. `pip3 install -r requirements.txt`: Install all the dependencies we used in this project.
3. Install NPM on your system:[DOWNLOAD](https://www.npmjs.com/package/npm)
4. `npm install`: install libraries for REACT.
6. `cd demo`
5. `python3 manage.py bower install`: install front-end packages.
7. `../node_modules/.bin/webpack --config webpack.config.js`: Compile front-end js with Webpack.
8. `python3 manage.py migrate`: Init Sqlite first, this is our Database.
9. `python3 manage.py crawler`: Crawl Novel and calculate those correlations between peoples.
10. `python3 manage.py network`: Calculate Social Network.
11. `python3 manage.py runserver`: Go to <http://127.0.0.1:8000> and see the demo page ~

## API

1. Showing all correlations in DB with this url pattern：`/api`
  - example:<http://127.0.0.1:8000/api>
  ```
  [
    [
      "令狐沖",
      "林平知",
      1
    ],
    [
      "岳不群",
      "東方不敗",
      2
    ]
  ]
  ```

## CMD

1. `python manage.py crawler`: get novel and insert character relationship into DB.
2. `python manage.py network`: calculate network info.
3. `python manage.py dump2csv`: dump DB into csv.