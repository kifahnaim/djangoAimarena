  document.addEventListener("DOMContentLoaded", function(event) {
    var customcolor = "#000000";
    var button = document.getElementById("button");
    var canvas = document.getElementById("canvas");
    var sound_enabled = true;
    var image_tracker = 'speaker';
    var svg = document.getElementById("countdown");
    var date;
    var playerLives = 5;
    var accuracyBuffer = 0;
    var shotsBuffer = 0;
    var hitsBuffer = 0;
    var gameActive = true;
    var targetX = 0,
        targetY = 0,
        shots = 0,
        hits = 0,
        accuracy = 0;
    var cursor = false;
    ctx = canvas.getContext('2d');

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
        this.explosionFrame = 9;
        this.width = 200;
        this.height = 200;
        if (sound_enabled){
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
            centreY = (this.y - 90) + (this.height / 2.1),
            hits = 0;

        for (i = 0; i < things.length; i++) {

            // If hit
            if (centreX > things[i].getX() && centreX < things[i].getX() + things[i].getWidth() &&
                centreY > things[i].getY() && centreY < things[i].getY() + things[i].getHeight() &&
                things[i].getHit() === false){
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




    function changeTarget(){
		target.src= 'target3.gif';
        closeNav();
	}


	function changeTarget1(){
		target.src= 'target2.gif';
        closeNav();
	}


    function changeTarget2(){
		target.src= 'target.gif';
        closeNav();
	}


    function loadSprite() {
		sprite = new Image();
		sprite.src = spriteurl;

        target = new Image();
        target.src = targeturl;

        explosion = new Image();
        explosion.src = explosionurl;
    }

	 fullscreen = function() {
	  var el = document.getElementById('canvas');

	  if (el.webkitRequestFullScreen) {
	    el.webkitRequestFullScreen();
	  } else {
	    el.mozRequestFullScreen();
	  }
	}

    function createThings() {
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

        for (var i = 0; i < 10; i++) {
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

    function gameover() {
        losingLives = setInterval(() => {

            if (playerLives <= 0) {
                document.getElementById("canvas").removeEventListener("mousemove", function(event) {
                    moveTarget()
                });

                $("#modalbtn").click();

                clearInterval(losingLives);
                clearInterval(moredotinterval);

                cleardots();
                var can = $("#canvas");
                $('#Screen').css('cursor', 'pointer');

                cursor = true;
                gameActive = false;
                savetodb();
            }
        });
    }

     restartgame=function() {
        ResetGlobalvariables();
        console.log("restart");
        $('.modal').modal({
            backdrop: 'static',
            keyboard: false
        });
        $(".modal").modal('toggle');
        ctx.fillStyle = "#cfcfcf";
        ctx.font = "bold 16pt Arial";
        ctx.fillText("Shots: " + " " + shots + " Hits: " + " " + hits + " Accuracy: " + " " + accuracy + "%", 10, 30);
        startGameAgain();

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

	 changeColorblue=function() {

	  customcolor = "#0033b5";
	}

	 changeColorwhite=function() {

	  customcolor = "#ffffff";
	}

	 dev=function() {
	  ctx.fillStyle = "red";
	}

	mainmenu = function() {
        window.location.href = homepage;
	}

    function ResetGlobalvariables() {
        accuracy = 0;
        shots = 0;
        hits = 0;
        playerLives = 5;
        accuracyBuffer = 0;
        shotsBuffer = 0;
        hitsBuffer = 0;
    }

     startGameAgain=function() {
        startGame()
        cursor = false;
        init();
        gameFrames();
        moreDots();
    }

   gameFrames= function () {
		clearCanvas();

		var img5 = document.getElementById("scream6");
		ctx.drawImage(img5, canvas.width - 120, canvas.height - 40);

		var img4 = document.getElementById("scream5");
		ctx.drawImage(img4, 10, canvas.height - 40);


		var img2 = document.getElementById("scream3");
		ctx.drawImage(img2, 10, 10);


		var img = document.getElementById("scream2");
		ctx.drawImage(img, (canvas.width / 2.5), (canvas.height / 3));

        for (i = 0; i < sprites.length; i++) {
            sprites[i].draw(ctx, sprite);
            sprites[i].checkBoundaryCollision();
            sprites[i].correctXY();
        }

        //console.log("requestanimframe");

        for (i = 0; i < explosions.length; i++) {
            explosions[i].draw(ctx, explosion);
            hits += explosions[i].checkHits(sprites);
        }

        if (shots > 0) {
            accuracy = Math.round((hits / shots) * 100);
            accuracy = accuracy > 100 ? 100 : accuracy < 0 ? 0 : accuracy;

            // Quick workaround to get missed.
            if (accuracyBuffer > accuracy || (hits == hitsBuffer && shots > shotsBuffer)) {
                playerLives--
            }
            accuracyBuffer  = accuracy
            hitsBuffer      = hits
            shotsBuffer     = shots
        }

		ctx.font = "18pt Bebas Neue";
		ctx.textBaseline = 'middle';
        ctx.fillStyle = "#cfcfcf";
		ctx.fillText("Shots:" + " " + shots + "  ", 40, 30);


		ctx.font = '18pt Bebas Neue';
		ctx.fillStyle = "#cfcfcf";
		ctx.fillText("Accuracy:" + " " + accuracy + "%", 50, canvas.height - 21);

		ctx.font = '10px serif';
		ctx.fillStyle = "#898989";
		ctx.fillText("Build" + " " + "11023.421", (canvas.width / 2), canvas.height - 14);

		ctx.font = '18pt Bebas Neue';
		ctx.fillStyle = "#cfcfcf";
		ctx.fillText("Hits:" + " " + hits, canvas.width - 80, canvas.height - 20);

        updatePlayerLife();

        document.getElementById("shots").value = shots;
        document.getElementById("accuracy").value = accuracy;
        document.getElementById("hits").value = hits;

        //Draw target
        if (!cursor) {
            ctx.drawImage(target, 0, 0, 512, 512,
                targetX - 50, targetY - 50,
                100, 100);
        }

        if (gameActive) {
            requestAnimationFrame(gameFrames);
        }
    }

     updatePlayerLife=function() {

        var totalHearts = '';

        // Count amount of hearts left
        for (var i = 0; i < playerLives; i++) {
            totalHearts = totalHearts + '&#10084;&#65039';
        }

        var lifeEl = document.getElementById('playerlife');
        if (playerLives <= 0) {
            lifeEl.innerHTML = ('DEAD 💀').fontsize(25)
            return
        }

        lifeEl.innerHTML = ('Lives: ' + totalHearts).fontsize(8).fontcolor("white");
    }

    function resizeCanvas() {
        var div = document.getElementById("Screen").offsetWidth;
        var div1 = document.getElementById("Screen").offsetHeight;

        canvas.width = window.innerWidth * 0.8;
        canvas.height = window.innerHeight * 0.8;
    }

	 showgametools=function() {
		var div = document.getElementById("gametools");
		$(div).slideDown("Slow");
	}

	 showgamecuztools=function() {
		var div = document.getElementById("openm");
		$(div).fadeTo(100, 1);
	}



    function moveTarget(e) {
        e = e || window.event;

        targetX = e.offsetX * canvas.width / canvas.clientWidth | 0;
        targetY = e.offsetY * canvas.width / canvas.clientWidth | 0;
    }

     fire=function() {
        explosions.push(new Explosion(targetX, targetY, new Audio(bang)));
        shots++;
    }

	 changetodefault =function(){
	sprite.src = defaults;
		closeNav()
	}

     toggleSound=function(){
        var image = document.getElementById('speaker');
        if(image_tracker=='speaker'){
            image.src= muteurl;
            image_tracker='mute';
        }else{
            image.src= speakerurl;
            image_tracker='speaker';
        }

        // Toggle sound
        sound_enabled = !sound_enabled
    }
      startGame=function() {
        // Set game state to active
        gameActive = true;
        gameover();
    }


     showCanvas=function() {
             init();
        gameFrames();
        moreDots();
        startGame();
            date=  formatDate(new Date());
                  console.log(date);
        button.style.display = "none";
        svg.style.display = "block";
        $("#disqus_thread").hide();
        setTimeout(function() {
            $("#countdown").fadeTo("slow", 0);
        }, 3000);
        setTimeout(function(){
            $(canvas).slideDown("fast", function(){
			showgametools();
			showgamecuztools();
		});
			playerlife.style.display = "block";
        }, 3500);
    }

	let colorInput = document.querySelector('#color');
	let hexInput = document.querySelector('#hex');

	colorInput.addEventListener('input', () =>{
		let color = colorInput.value;
		hexInput.value = color;
		customcolor = color;
	});

/* Set the width of the sidebar to 250px and the left margin of the page content to 250px */
	 openNav=function() {
		document.getElementById("mySidebar").style.width = "350px";
		document.getElementById("openm").style.marginLeft = "300px";
		document.getElementById("side").style.opacity = "1";
		document.getElementById("openm").style.opacity = "0";
	}

  /* Set the width of the sidebar to 0 and the left margin of the page content to 0 */
	 closeNav=function() {
		document.getElementById("mySidebar").style.width = "0";
		document.getElementById("openm").style.marginLeft = "0";
		document.getElementById("openm").style.opacity = "1";
		document.getElementById("side").style.opacity = "0";
	}



    // resize the canvas to fill browser window dynamically
    window.addEventListener('resize', resizeCanvas, false);
    canvas.addEventListener('click', function(event) {
        fire();
    })

    canvas.addEventListener('mousemove', function(event) {
        moveTarget()
    })





     savetodb=function(){
        var Gamemodeid = 3 ;
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
				document.getElementById('scoretext').innerHTML = Math.round(response["score"]);
				document.getElementById('accuracytext').innerHTML = Math.round(response["Accuracy"]);
				document.getElementById('facebook').setAttribute("href", "https://www.facebook.com/sharer/sharer.php?u=aimarena.com&quote=I got " + response['score'] + " xp on AIMARENA");
				document.getElementById('twitter').setAttribute("href", "https://twitter.com/intent/tweet?via=aimarena&text=I got "+ response['score'] +" xp on AIMARENA" );
				if (response["rankimage"]) {
					console.log("image");
					$("#imagemodal").html("<center><img width='20%' height='20%' id='rankimage' src=/media/" + response["rankimage"] + "><br></center>");
				}
					if (response["showanimation"]) {
					$("#congrats").html('Congratulations! <br> You achieved a new Rank');
					$("#congrats").parent().removeClass('demo2ovr');
                    $('#scoretext').css("color", "white");
                    $('#accuracytext').css("color", "white");
                                        $('#h2accuracy').css("color", "white");
                    $('#h2score').css("color", "white");
				}
            },
            error: function(rs, e){
                console.log("error occured");
            },
        });
    }
});
    $(document).ready(function(){
        $("#hidestats").click(function(){
            $("#hideme").hide(500);
            $("#hidestats").hide(00);
            $("#showstats").show(00);
        });
    });

    $(document).ready(function(){
        $("#showstats").click(function(){
            $("#hideme").show(500);
            $("#showstats").hide(00);
            $("#hidestats").show(00);
        });
    });

