var express = require('express');
var parser = require('body-parser');
var app = express();

app.use(parser.urlencoded({ extended: false }))
app.use(parser.json())
 
app.use(function(req,res,next){
    res.locals.userValue = null;
    next();
})
 

app.set('view engine', 'ejs');
app.set('views', __dirname + '/views');

const mongoose = require('mongoose');
mongoose.connect('mongodb://localhost/name_of_your_DB', {useNewUrlParser: true});

const UserSchema = new mongoose.Schema({
    name: String,
    quote: String,
    created_on : {type: Date, default: Date.now },
 },{timestamps: true });
   // create an object to that contains methods for mongoose to interface with MongoDB
   const User = mongoose.model('User', UserSchema);
   

   app.get('/', (req, res) => {  
        User.find()
            .then(data => res.render("index", {users: data}))
            .catch(err => res.json(err));
    });



app.post('/quote', (req, res) => {
    console.log("hi")
    console.log(req.body.name)
    const user = new User();
    user.name = req.body.name;
    user.quote = req.body.text;
    user.save()
      .then(newUserData => console.log('user created: ', newUserData))
      .catch(err => console.log(err));
    res.redirect('/quotes');
  })

  app.get('/quotes', (req, res) => {  
    arr = User.find({}, function(err, quotes) {
        res.render('quotes', {arr:quotes});
      }).sort({createdAt:-1});
    });





app.listen(8000, () => console.log("listening on port 8000"));

