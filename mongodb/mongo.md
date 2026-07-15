emp
id, name
1, e1
2, e2
- select * from emp => db.emp.find()
- select * from emp where id=1 => db.emp.find({"id": 1}, {})
- select name from emp where id=2 => db.emp.find({"id": 2}, {"name": 1})
- select name from emp => db.emp.find({}, {"name": 11})
- select * from emp where id > 1 => db.emp.find({"id": {$gt: 1}}, {})
- select * from emp where id in (1, 2) => db.emp.find({id: {$in: [1, 2]}})
- select * from emp where id not in (1, 2) => db.emp.find({id: {$nin: [1, 2]}})
- select * from emp where id = 1 and name = 'e1' => db.emp.find({$and: [  {"id": 1}, {"name": "e1"}] }, {})
- select * from emp where id = 1 or name = 'e1' => db.emp.find({$or: [  {"id": 1}, {"name": "e1"}] }, {})

SQL where clause is 'where likes>10 AND (by = 'bootcamp' OR title = 'MongoDB Overview')'
``` db.mycol.find({"likes": {$gt:10}, $or: [{"by": "bootcamp"}, {"title": "MongoDB Overview"}]}).pretty() ```

``` count(*) group by _id ```
db.mycol.aggregate([{$group : {_id : "$by", sumofLikes : {$sum : 1}}}])

db.mycol.aggregate([{$group : {_id : "$by", sumofLikes : {$sum : "$likes"}}}])

db.mycol.aggregate([{$group : {_id : "$by", minLikes : {$min : "$likes"}}}])

Create Index
db.mycol.createIndex({"title": 1}) -- 1 means create index in ascending, -1 is descending

Drop index
db.mycol.dropIndex({"title": 1})