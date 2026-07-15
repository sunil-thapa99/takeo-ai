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