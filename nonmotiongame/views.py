import json
from datetime import datetime

from django.contrib import messages
from django.db import connection
from django.http import JsonResponse
from django.shortcuts import render, redirect
from idna import unicode

from authapp.models import Userreg, admin_actions
from .models import Game, Game_Mode, Game_Statistics, User_Info, Rank, products, userproducts, GameMode_User


# Create your views here.
def nonmotiongame(request):
    return render(request, "nonmotiongame.html")


def savescore(request):
    if request.method == "POST" and request.is_ajax():
        showanimation = False
        beforechangeinfo = None
        afterchangeinfo = None
        startdate = request.POST.get("startdate")
        shots = request.POST.get("shots")
        Gamemodeid = request.POST.get("Gamemodeid")
        print("Gamemodeid")
        print(Gamemodeid)
        hits = request.POST.get("hits")
        accuracy = request.POST.get("accuracy")
        userid = request.session.get("userid")
        Games = Game()
        Games.Game_Mode_ID = Game_Mode(Gamemodeid)
        Games.User_ID = Userreg(userid)
        Games.Start_Date = startdate
        Games.End_Date = datetime.now()
        Games.save()

        gameid = Game.objects.get(Game_Mode_ID=Game_Mode(Gamemodeid), User_ID=Userreg(userid), Start_Date=startdate,
                                  End_Date=Games.End_Date)
        Gamestat = Game_Statistics()
        Gamestat.Shot = shots
        Gamestat.Hit = hits
        Gamestat.Accuracy = accuracy
        Gamestat.Score = (float(hits) * float(accuracy)) / 10
        Gamestat.Game_ID = gameid
        Gamestat.save()
        print("allstats")
        allstatistics = Game_Statistics.objects.filter(Game_ID__User_ID=Userreg(request.session.get('userid')))
        Gamemodestats = Game_Statistics.objects.filter(Game_ID__User_ID=Userreg(request.session.get('userid')),
                                                       Game_ID__Game_Mode_ID_id=Gamemodeid)
        print("Gamemodestats")
        print(Gamemodestats)

        counstats = allstatistics.count()
        countGamemodestats = Gamemodestats.count()
        sumavgpermode = 0
        sumscoreavgpermode = 0
        sumhitspermode = 0
        sumshotspermode = 0
        if Gamemodeid == str(1):
            if countGamemodestats >= 6:
                beforechangeinfo = GameMode_User.objects.values_list('Rank_id', flat=True).get(User_ID_id=userid,
                                                                                               Game_Mode_ID=Gamemodeid)

        for i in Gamemodestats:
            print(i.Accuracy)
            sumavgpermode = sumavgpermode + i.Accuracy
            sumscoreavgpermode = sumscoreavgpermode + i.Score
            sumhitspermode = sumhitspermode + float(i.Hit)
            sumshotspermode = sumshotspermode + float(i.Shot)

        averageaccpermode = round(sumavgpermode / countGamemodestats, 3)
        averagescorepermode = round(sumscoreavgpermode / countGamemodestats, 3)
        averagehitspermode = round(sumhitspermode / countGamemodestats, 3)
        averageshotspermode = round(sumshotspermode / countGamemodestats, 3)
        if GameMode_User.objects.filter(User_ID=request.session.get("userid"), Game_Mode_ID=Gamemodeid).count() < 1:
            pergamemode = GameMode_User()
            pergamemode.User_ID = Userreg(userid)
            pergamemode.Hits_Avg = averagehitspermode
            pergamemode.Shots_Avg = averageshotspermode
            pergamemode.Score_Avg = averagescorepermode
            pergamemode.Game_Mode_ID = Game_Mode(Gamemodeid)
            pergamemode.Accuracy_Avg = averageaccpermode
            pergamemode.save()
        else:
            GameMode_User.objects.filter(User_ID=request.session.get("userid"), Game_Mode_ID=Gamemodeid).update(
                Accuracy_Avg=averageaccpermode,
                Score_Avg=averagescorepermode,
                Shots_Avg=averageshotspermode,
                Hits_Avg=averagehitspermode)
        scoresforranks = GameMode_User.objects.filter(User_ID=request.session.get("userid"), Game_Mode_ID=Gamemodeid)
        rankminmax = Rank.objects.all()
        rankimage = None
        sumavg = 0
        sumscoreavg = 0
        sumhits = 0
        sumshots = 0

        for i in allstatistics:
            print(i.Accuracy)
            sumavg = sumavg + i.Accuracy
            sumscoreavg = sumscoreavg + i.Score
            sumhits = sumhits + float(i.Hit)
            sumshots = sumshots + float(i.Shot)
        print(sumscoreavg)
        print("sum")
        print(sumavg)
        print(counstats)
        averageacc = round(sumavg / counstats, 3)
        averagescore = round(sumscoreavg / counstats, 3)
        averagehits = round(sumhits / counstats, 3)
        averageshots = round(sumshots / counstats, 3)
        print("avg")
        print(averageacc)
        print(averagehits)
        print(averageshots)

        userinfobefore = User_Info.objects.filter(User_ID=request.session.get("userid")).count()

        if userinfobefore < 1:
            infouser = User_Info()
            infouser.User_ID = Userreg(request.session.get("userid"))
            infouser.Accuracy_Avg = averageacc
            infouser.Score_Avg = averagescore
            infouser.Hits_Avg = averagehits
            infouser.Shots_Avg = averageshots
            infouser.forumpoints = 0
            infouser.save()


        else:
            User_Info.objects.filter(User_ID=request.session.get("userid")).update(Accuracy_Avg=averageacc,
                                                                                   Score_Avg=averagescore,
                                                                                   Shots_Avg=averageshots,
                                                                                   Hits_Avg=averagehits)

        print("before")

        print(beforechangeinfo)

        if countGamemodestats >= 5:
            print('greater than 5')
            print(Gamemodeid)
            if Gamemodeid == str(1):
                print("id=1")

                if scoresforranks:
                    for i in rankminmax:
                        for item in scoresforranks.values('Score_Avg'):
                            print(item["Score_Avg"])
                            if i.score_min <= item["Score_Avg"] < i.score_max:
                                rankimage = i.Rank_image
                                GameMode_User.objects.filter(User_ID_id=userid, Game_Mode_ID=Gamemodeid).update(
                                    Rank_id=i.id)
                                if countGamemodestats >= 6:
                                    afterchangeinfo = GameMode_User.objects.values_list('Rank_id', flat=True).get(
                                        User_ID_id=userid,
                                        Game_Mode_ID=Gamemodeid)
                                print("after")

                                print(afterchangeinfo)
                                if countGamemodestats >= 6:
                                    if afterchangeinfo > beforechangeinfo:
                                        showanimation = True
                                print(rankimage)
                                print(showanimation)

                    return JsonResponse(
                        {"Avgacc": averageaccpermode, "Avgscore": averagescorepermode,
                         "score": (float(hits) * float(accuracy)) / 10,
                         "Accuracy": accuracy, "rankimage": (str(rankimage)), "showanimation": showanimation})
            else:
                return JsonResponse(
                    {"Avgacc": averageaccpermode, "Avgscore": averagescorepermode,
                     "score": (float(hits) * float(accuracy)) / 10,
                     "Accuracy": accuracy})
        else:
            print('less than 5')
            return JsonResponse(
                {"Avgacc": averageaccpermode, "Avgscore": averagescorepermode,
                 "score": (float(hits) * float(accuracy)) / 10,
                 "Accuracy": accuracy})

    return JsonResponse({"message": "fail"})


def shop(request):
    image = None
    if request.session.get("userid"):
        userid=request.session.get("userid")
        image = Userreg.objects.get(id=userid).user_thumbnail
    context = {"products": products.objects.all(),
               "userdetails": User_Info.objects.filter(User_ID_id=request.session.get("userid")),
               "image": image}
    return render(request, "shop.html", context)


def purchase(request, pk):
    if request.method == "POST" and request.is_ajax():
        product_id = request.POST.get("product_id")
        product_price = request.POST.get("product_price")
        userinfo = User_Info.objects.values_list('forumpoints', flat=True).get(User_ID_id=request.session.get("userid"))
        print(product_price)
        print(userinfo)
        try:
            productexist = userproducts.objects.values_list('product_id', flat=True).get(
                user_id=request.session.get("userid"), product_id=product_id)
        except:
            productexist = 0000000000000000000
        print(productexist)
        print(product_id)
        if int(productexist) == int(product_id):
            return JsonResponse({"nopoints": "Product already exists !"})
        else:
            if userinfo >= product_price:
                saverecord = userproducts()
                saverecord.product = products(product_id)
                saverecord.user = Userreg(request.session.get("userid"))
                saverecord.save()
                userpoints = int(userinfo) - int(product_price)
                print(userpoints)
                User_Info.objects.filter(User_ID_id=request.session.get("userid")).update(forumpoints=userpoints)
                return JsonResponse({"nopoints": "You purchased a new product !", "userpoints": userpoints})
            else:
                return JsonResponse({"nopoints": "Sorry you don't have enough points to buy !"})
    return JsonResponse({"message": "fail"})


def bannedfromgame(request):
    banned = None
    if request.session.get("userid"):

        banned = admin_actions.objects.values_list('user_ban_game', flat=True).filter(
            user_id=request.session.get("userid"))
        print("kifahnaim")
        print(banned)
    return {"banned": banned}


def survival(request):
    if request.session.get("userid") and request.session.get('RoleName') == "User":
        userid = request.session.get("userid")
        var = Game_Statistics.objects.filter(Game_ID__Game_Mode_ID=1, Game_ID__User_ID=userid).order_by('-Date')[
              0:6]
        sprites = userproducts.objects.filter(user_id=request.session.get("userid"))
        Userdetails = Userreg.objects.get(id=userid).user_thumbnail
        banned = admin_actions.objects.values_list('user_ban_game', flat=True).filter(
            user_id=request.session.get("userid"))
        print("banned1")
        print(banned)
        for i in banned:
            if i:
                print("banned2")
                print(i)
                return redirect('game')
            else:

                return render(request, "survivalgame.html", {"sprites": sprites, "lastmatches": var,"Userdetails":Userdetails})
        return render(request, "survivalgame.html",
                      {"sprites": sprites, "lastmatches": var, "Userdetails": Userdetails})
    else:
        return redirect('game')


def casual(request):
    if request.session.get("userid") and request.session.get('RoleName') == "User":
        userid = request.session.get("userid")
        var = Game_Statistics.objects.filter(Game_ID__Game_Mode_ID=2, Game_ID__User_ID=userid).order_by('-Date')[
              0:6]
        sprites = userproducts.objects.filter(user_id=request.session.get("userid"))
        Userdetails = Userreg.objects.get(id=userid).user_thumbnail
        banned = admin_actions.objects.values_list('user_ban_game', flat=True).filter(
            user_id=request.session.get("userid"))
        print("banned")
        print(banned)
        for i in banned:
            if i:
                print(banned)
                return redirect('game')

            else:

                return render(request, "casual.html", {"sprites": sprites, "lastmatches": var,"Userdetails":Userdetails})
        return render(request, "casual.html",
                      {"sprites": sprites, "lastmatches": var, "Userdetails": Userdetails})
    else:
        return redirect('game')


def lives(request):
    if request.session.get("userid") or request.session.get('RoleName') == "User":
        userid = request.session.get("userid")
        Userdetails = Userreg.objects.get(id=userid).user_thumbnail
        var = Game_Statistics.objects.filter(Game_ID__Game_Mode_ID=3, Game_ID__User_ID=userid).order_by('-Date')[
              0:6]
        sprites = userproducts.objects.filter(user_id=request.session.get("userid"))
        banned = admin_actions.objects.values_list('user_ban_game', flat=True).filter(
            user_id=request.session.get("userid"))
        print("banned")
        print(banned)
        for i in banned:
            if i:
                print(banned)
                return redirect('game')

            else:

                return render(request, "lives.html", {"sprites": sprites, "lastmatches": var,"Userdetails":Userdetails})
        return render(request, "lives.html",
                      {"sprites": sprites, "lastmatches": var, "Userdetails": Userdetails})

    else:
        return redirect('game')