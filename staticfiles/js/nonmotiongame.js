var date;
document.addEventListener("DOMContentLoaded", function(event) {

   var canvas = document.getElementById('canvas');
        ctx = canvas.getContext('2d');
        var targetX = 0,
            targetY = 0,
            shots = 0,
            hits = 0,
            accuracy = 0,
            timerseconds = 60;
        var cursor = false,
            active = true;


        function Thing(mapX, mapY, x, y, canvas) {
            this.x = x;
            this.y = y;
            this.mapX = mapX;
            this.mapY = mapY;
            this.height = 50;
            this.width = 50;
            this.canvas = canvas;
            this.hit = false;
        };
        const mouse = {
            x: undefined,
            y: undefined
        }


        Thing.prototype.draw = function(ctx, sprite) {

            if (this.hit === false) {

                ctx.drawImage(sprite, this.getMapX(), this.getMapY(),
                    90, 90,
                    this.getX(), this.getY(),
                    this.getWidth(), this.getHeight());
            }

            return this;
        };


        Thing.prototype.toRad = function(v) {
            return v * Math.PI / 180;
        };

        Thing.prototype.checkBoundaryCollision = function() {

            if (this.x + this.width > this.canvas.width ||
                this.x < 0) {
                this.direction = 2 * 0 - this.direction - 180;
            } else if (this.y < 0 ||
                this.y + this.height > this.canvas.height) {
                this.direction = 2 * 90 - this.direction - 180;
            }
        };

        Thing.prototype.correctXY = function() {

            if (this.x + this.width >= this.canvas.width) {
                this.x = this.canvas.width - this.width;
            } else if (this.x < 0) {
                this.x = 0;
            } else if (this.y < 0) {
                this.y = 0;
            } else if (this.y + this.height >= this.canvas.height) {
                this.y = this.canvas.height - this.height;
            }
        };

        Thing.prototype.getX = function() {
            return this.x;
        };

        Thing.prototype.getY = function() {
            return this.y;
        };

        Thing.prototype.getMapX = function() {
            return this.mapX;
        };

        Thing.prototype.getMapY = function() {
            return this.mapY;
        };

        Thing.prototype.getWidth = function() {
            return this.width;
        };

        Thing.prototype.getHeight = function() {
            return this.height;
        };

        Thing.prototype.setHit = function() {
            this.hit = true;
        };

        Thing.prototype.getHit = function() {
            return this.hit;
        };

        function Explosion(x, y, audio) {

            this.x = x;
            this.y = y;
            this.drawing = true;
            this.explosionFrame = 15;
            this.width = 200;
            this.height = 200;

            audio.play();

        };

        Explosion.prototype.getDrawing = function() {

            return this.drawing;

        };

        Explosion.prototype.checkHits = function(things) {

            if (this.drawing === false) {
                return 0;
            }

            var centreX = (this.x - 100) + (this.width / 2),
                centreY = (this.y - 90) + (this.height / 2),
                hits = 0;

            for (i = 0; i < things.length; i++) {

                if (centreX > things[i].getX() &&
                    centreX < things[i].getX() + things[i].getWidth() &&
                    centreY > things[i].getY() &&
                    centreY < things[i].getY() + things[i].getHeight() &&
                    things[i].getHit() === false) {

                    things[i].setHit();

                    hits++;

                }
            }

            return hits;
        };

        Explosion.prototype.draw = function(ctx, explosion) {

            if (this.drawing === false) {
                return this;
            }

            try {

                if (this.explosionFrame-- <= 0) {
                    this.drawing = false;
                }

                //Draw explostion
                ctx.drawImage(explosion, ((this.explosionFrame % 10) - 1) * 65, 0,
                    65, 65,
                    this.x - 100, this.y - 90,
                    this.width, this.height);

            } catch (e) {

            }
            return this;

        };



        var explosions = [],
            ctx, canvas, sprites = [],
            sprite = null;

        function loadSprite() {

            sprite = new Image();
            sprite.src = spriteurl;

            target = new Image();
            target.src = targeturl;

            explosion = new Image();
            explosion.src = explosionurl;

        }

        function createThings() {

            var i;

            spriteMap = [
                [0, 120],
                [140, 120],
                [270, 120],
                [270, 250],
                [400, 120],
                [400, 250],
                [530, 250],
                [530, 120]
            ];

            for (i = 0; i < 10; i++) {
                sprites.push(createThing(spriteMap));
            }
        }

        function createThing(spriteMap) {

            var cur, map = spriteMap[Math.floor(Math.random() *
                (spriteMap.length - 1))];

            cur = new Thing(
                map[0],
                map[1],
                Math.floor((Math.random() * canvas.width) + 1),
                Math.floor((Math.random() * canvas.height) + 1),
                canvas
            );

            return cur;
        }

        function init() {



            resizeCanvas();
            loadSprite();
            createThings();
        }

        function clearCanvas() {

            ctx.fillStyle = "black";
            ctx.fillRect(0, 0, canvas.width, canvas.height);

        }

        function myFunction(ele) {
            console.log(ele);
            ele.setHit();

        };


        function moreDots() {

            moredotinterval = setInterval(() => {

                console.log("moredots");
                cleardots();



                createThings();

            }, 5000)



        }

        function cleardots() {
            sprites.forEach(myFunction);
        }

         function dateComponentPad(value) {
          var format = String(value);

          return format.length < 2 ? '0' + format : format;
        }

            function formatDate(date) {
              var datePart = [ date.getFullYear(), date.getMonth() + 1, date.getDate() ].map(dateComponentPad);
              var timePart = [ date.getHours(), date.getMinutes(), date.getSeconds() ].map(dateComponentPad);

              return datePart.join('-') + ' ' + timePart.join(':');
            }


        function downcountimer() {
            countDownTimer = setInterval(() => {
                  if  (timerseconds == 60) {
                  date=  formatDate(new Date());
                  console.log(date);
                }
                timerseconds =
                    Number(timerseconds) - 1;

                if (timerseconds == 50) {

                    document.getElementById("canvas").removeEventListener("mousemove", function(event) {
                        moveTarget()
                    });
                    console.log("timer");
                    $("#modalbtn").click();
                    clearInterval(countDownTimer);
                    clearInterval(moredotinterval);

                    cleardots();
                    var can = $("#canvas");
                    $('#Screen').css('cursor', 'pointer');
                    var mainmenubtn = document.getElementById('Mainmenu');
                    var restartgamebtn = document.getElementById('RestartGame');
                    mainmenubtn.addEventListener("click", mainmenu);
                    restartgamebtn.addEventListener("click", restartgame);
                    cursor = true;
                    active = false;
                    console.log(active);
                    savetodb();

                }


            }, 1000);



        }

        function restartgame() {


            ResetGlobalvariables();
            console.log("restart");
            $('.modal').modal({
                backdrop: 'static',
                keyboard: false
            });
            $(".modal").modal('toggle');
            clearCanvas();
            ctx.fillStyle = "#cfcfcf";
            ctx.font = "bold 16pt Arial";
            ctx.fillText("Timer:" + " " + timerseconds + "  " + "Shots: " + " " + shots + " Hits: " + " " + hits +
                " Accuracy: " + " " + accuracy + "%", 10, 30);
            startgameagain();

        }

        function mainmenu() {

        }

        function ResetGlobalvariables() {
            timerseconds = 60;
            accuracy = 0;
            shots = 0;
            hits = 0;

        }

        function startgameagain() {
            cursor = false;
            active = true;
            init();
            start();
            moreDots();
            downcountimer();

        }



        downcountimer();

        function start() {


            clearCanvas();


            for (i = 0; i < sprites.length; i++) {
                sprites[i].draw(ctx, sprite);
                sprites[i].checkBoundaryCollision();
                sprites[i].correctXY();

            }
            console.log("requestanimframe");

            for (i = 0; i < explosions.length; i++) {
                explosions[i].draw(ctx, explosion);
                hits += explosions[i].checkHits(sprites);
            }

            if (shots > 0) {
                accuracy = Math.round((hits / shots) * 100);
                accuracy = accuracy > 100 ? 100 : accuracy < 0 ? 0 : accuracy;
            }


            ctx.fillStyle = "#cfcfcf";
            ctx.font = "bold 16pt Arial";
            ctx.fillText("Timer:" + " " + timerseconds + "  " + "Shots: " + " " + shots + " Hits: " + " " + hits +
                " Accuracy: " + " " + accuracy + "%", 10, 30);
            document.getElementById("shots").value = shots;
            document.getElementById("accuracy").value = accuracy;
            document.getElementById("hits").value = hits;
            //Draw target
            if (cursor == false) {
                ctx.drawImage(target, 0, 0, 512, 512,
                    targetX - 50, targetY - 50,
                    100, 100);
            }

            if (active) {
                requestAnimationFrame(start);
            }



        }


        function resizeCanvas() {

            ctx.canvas.width = window.innerWidth;
            ctx.canvas.height = window.innerHeight;

        }



        function moveTarget(e) {

            e = e || window.event;

            targetX = e.pageX;
            targetY = e.pageY;

        }


        function fire() {

            explosions.push(new Explosion(targetX, targetY, new Audio(bang)));
            shots++;
        }

        // resize the canvas to fill browser window dynamically
        window.addEventListener('resize', resizeCanvas, false);
        canvas.addEventListener('click', function(event) {
            fire();
        })

        canvas.addEventListener('mousemove', function(event) {
            moveTarget()
        })

        // Start the process
        window.onload = function() {
            init();
            start();
            moreDots();
        };

});


function savetodb(){
                var Gamemodeid = 1 ;

                var shots =  $("#shots").val();
                var hits =  $("#hits").val();
                var accuracy =  $("#accuracy").val();



                $.ajax({
                    type: 'POST',
                    url: saveurl,
                    data: {
                    'startdate':date,
                    'Gamemodeid' :Gamemodeid,
                    'shots':shots,
                    'hits':hits,
                    'accuracy':accuracy,
                    'csrfmiddlewaretoken': csrftoken,
                     },
                    dataType: 'json',
                    success: function(response){
                        console.log("save worked");
                        console.log(response["score"]);
                        document.getElementById('scoretext').innerHTML =Math.round(response["score"]);
                        document.getElementById('accuracytext').innerHTML = Math.round(response["Accuracy"]);
                        if(response["rankimage"]){
                        $("#rankimage").attr("src","/media/" +response["rankimage"] );
                         }
                    },
                    error: function(rs, e){
                        console.log("error occured");
                    },
                });




}




