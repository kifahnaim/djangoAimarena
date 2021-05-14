document.addEventListener("DOMContentLoaded", function(event) {
    let colorInput = document.querySelector('#color');
    let hexInput = document.querySelector('#hex');
    
    
    
    var canvas = document.getElementById("canvas");
    var screen = document.getElementById("screen");
    
    
    
    var customcolor = "#000000";
            var text = "Hello Demo";
    
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
                this.height = 60;
                this.width = 60;
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
                this.explosionFrame = 5;
                this.width = 200;
                this.height = 200;
                if (sound_enabled== "true"){
                audio.play();
                }
    
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
                ctx, canvas, sprites = [];
    
    
    
    
    
    
    
    
    
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
                    [270, 120],
                    [270, 250],
                    [400, 120],
                    [400, 250],
                    [530, 250],
                    [530, 120],
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
    
    ctx.fillStyle = customcolor;
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    
    }
    
    
            function myFunction(ele) {
    
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
    
                        mainmenubtn.addEventListener("click", mainmenu);
    
                        cursor = true;
                        active = false;
                        console.log(active);
                        savetodb();
    
                    }
    
    
                }, 1000);
                }
    
             restartgame= function() {
    
                ResetGlobalvariables();
                console.log("restart");
    
                clearCanvas();
                ctx.fillStyle = "#cfcfcf";
                ctx.font = "bold 16pt Arial";
    
                ctx.fillText("Timer:" + " " + timerseconds + " " + "Shots:" + " " + shots + " Hits:" + " " + hits +
                    " Accuracy:" + " " + accuracy + "%", 10, 30);
                startgameagain();
                document.getElementById('scoretext').innerHTML = '';
    document.getElementById('accuracytext').innerHTML ='';
      $("#imagemodal").html('');
            }
    
            function mainmenu() {
    
            }
    
    
            function dev() {
                ctx.fillStyle = "red";
    }
    
    
    
    
    
            function ResetGlobalvariables() {
                timerseconds = 60;
                accuracy = 0;
                shots = 0;
                hits = 0;
    
            }
    
             startgameagain= function() {
            console.log("stargameagain")
                cursor = false;
                active = true;
                init();
                start();
                moreDots();
                downcountimer();
    
            }
    
    
    
    
    
            function start() {
    
    
                clearCanvas();
    
    
                var img5 = document.getElementById("scream6");
    
    ctx.drawImage(img5, canvas.width - 120, canvas.height - 40);
    
    
                var img4 = document.getElementById("scream5");
    
    ctx.drawImage(img4, 10, canvas.height - 40);
    
    
                var img3 = document.getElementById("scream4");
    
    ctx.drawImage(img3, canvas.width - 120 , 10);
    
    
    
    
    
    
                var img2 = document.getElementById("scream3");
    
    ctx.drawImage(img2, 10, 10);
    
    
                var img = document.getElementById("scream2");
    
    ctx.drawImage(img, (canvas.width/2.5) , (canvas.height/3));
    
                for (i = 0; i < sprites.length; i++) {
                    sprites[i].draw(ctx, sprite);
                    sprites[i].checkBoundaryCollision();
                    sprites[i].correctXY();
    
                }
    
    
                for (i = 0; i < explosions.length; i++) {
                    explosions[i].draw(ctx, explosion);
                    hits += explosions[i].checkHits(sprites);
                }
    
                if (shots > 0) {
                    accuracy = Math.round((hits / shots) * 100);
                    accuracy = accuracy > 100 ? 100 : accuracy < 0 ? 0 : accuracy;
                }
    
    
    
    
    
                ctx.fillStyle = "#cfcfcf";
                ctx.font = "18pt Bebas Neue";
                ctx.textBaseline = 'middle';
                ctx.fillText("Shots:" + " " + shots + "  ", 40, 30);
    
    
               // ctx.fillText("Timer:" + " " + timerseconds + "  " + "Shots: " + " " + shots + " Hits: " + " " + hits +
                   // " Accuracy: " + " " + accuracy + "%", 10, 30);
    
    
    
    
                    ctx.font = '18pt Bebas Neue';
    
                    ctx.fillStyle = "#cfcfcf";
                    ctx.fillText("Timer:" + " " + timerseconds, canvas.width - 90 , 30);
    
    
    
                    ctx.font = '18pt Bebas Neue';
    
       ctx.fillStyle = "#cfcfcf";
       ctx.fillText("Accuracy:" + " " + accuracy, 50, canvas.height - 21);
    
    
                    ctx.font = '10px serif';
    
       ctx.fillStyle = "#898989";
       ctx.fillText("Build" + " " + "11023.421", (canvas.width/2) , canvas.height - 14);
    
    
       ctx.font = '18pt Bebas Neue';
    
       ctx.fillStyle = "#cfcfcf";
       ctx.fillText("Hits:" + " " + hits, canvas.width - 80 , canvas.height - 20);
    
    
    
    
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
    
                var div = document.getElementById("Screen").offsetWidth;
                var div1 = document.getElementById("Screen").offsetHeight;
    
                canvas.width = window.innerWidth * 0.8;
                canvas.height = window.innerHeight * 0.8;
    
            }
    
    
    
            function moveTarget(e) {
    
    
                e = e || window.event;
    
                targetX = e.offsetX * canvas.width / canvas.clientWidth | 0;
                targetY = e.offsetY * canvas.width / canvas.clientWidth | 0;
    
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
    
    
    
    
              $("#hidestats").click(function(){
        $("#hideme").hide(500);
        $("#hidestats").hide(00);
        $("#showstats").show(00);
    
      });
    
      $("#showstats").click(function(){
        $("#hideme").show(500);
        $("#showstats").hide(00);
        $("#hidestats").show(00);
      });
    colorInput.addEventListener('input', () =>{
        let color = colorInput.value;
        hexInput.value = color;
        customcolor = color;
    });
    showCanvas = function() {
      var button = document.getElementById("button");
                init();
                start();
                moreDots();
                setTimeout(function(){
                    downcountimer();
                    console.log("started timer now");
                     }, 3000);
    var svg = document.getElementById("countdown");
        button.style.display="none";
        svg.style.display="block";
        setTimeout(function() {
            $("#countdown").fadeTo("slow", 0);
            }, 3000);
        setTimeout(function(){
    
    $(canvas).slideDown( "fast", function() {
    
        showgametools();
        showgamecuztools();
    
      });
    
    }, 3500);
    
    
    }
    
         changeTarget=function(){
            target.src= target3;
            closeNav();
        }
    
    
         changeTarget1=function(){
            target.src= target2;
            closeNav();
        }
    
    
        changeTarget2=function (){
            target.src= target1;
            closeNav();
        }
    
    
    
    
             changeColor=function() {
                var inputVal = document.getElementById("colorinput").value;
                console.log("inputVal");
                customcolor = inputVal;
            }
    
    
    
             changecolorblack=function() {
    
               customcolor = "#000000";
           }
    
    
            changecolorgrey=function() {
    
               customcolor = "#848484";
           }
    
             changeColorred=function() {
    
                customcolor = "#c40000";
            }
    
             changeColorblue =function() {
    
               customcolor = "#0033b5";
           }
    
            changeColorwhite=function() {
    
               customcolor = "#ffffff";
           }
    });
    
    
    
            function showgametools() {
    
    var div = document.getElementById("gametools");
    
    
    $(div).slideDown("Slow");
    
    //div.style.display = "block";
    
    
    }
    
    
    
    function showgamecuztools() {
    
    var div = document.getElementById("openm");
    
    
    $(div).fadeTo(100, 1);
    
    //div.style.display = "block";
    
    
    }
    
    
    
    
    
    /* Set the width of the sidebar to 250px and the left margin of the page content to 250px */
    function openNav() {
        document.getElementById("mySidebar").style.width = "350px";
        document.getElementById("openm").style.marginLeft = "300px";
        document.getElementById("side").style.opacity = "1";
        document.getElementById("openm").style.opacity = "0";
    
      }
    
      /* Set the width of the sidebar to 0 and the left margin of the page content to 0 */
      function closeNav() {
        document.getElementById("mySidebar").style.width = "0";
        document.getElementById("openm").style.marginLeft = "0";
        document.getElementById("openm").style.opacity = "1";
        document.getElementById("side").style.opacity = "0";
      }
    
            var sound_enabled = "true" ;
            var image_tracker = 'speaker';
            var sprite = null;
    
    
    
    
    
    
           function changeSprite(spriteinput){
           console.log("spriteinput");
           console.log(spriteinput);
            sprite.src= spriteinput;
            closeNav();
            }
    
    
            function fullscreen(){
               var el = document.getElementById('canvas');
    
               if(el.webkitRequestFullScreen) {
                   el.webkitRequestFullScreen();
               }
              else {
                 el.mozRequestFullScreen();
              }
    }
    
    
    
    
            function change(){
    
                var image = document.getElementById('speaker');
                if(image_tracker=='speaker'){
                image.src=muteurl;
                image_tracker='mute';
            }
             else{
             image.src=speakerurl;
             image_tracker='speaker';
                }
                    if (sound_enabled == "true"){
                    sound_enabled= "false";
                    }
                    else{
                    sound_enabled = "true";
                    }
             }
    
    var date;
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
                            console.log("image");
                            $("#imagemodal").html("<center><img width='20%' height='20%' id='rankimage' src=/media/"+response["rankimage"]+"><br></center>");
                             }
                             if (response["showanimation"]){
                             $("#congrats").html('Congratulations! <br> You achieved a new Rank')
                             }
                        },
                        error: function(rs, e){
                            console.log("error occured");
                        },
                    });
    
    
    
    
    }