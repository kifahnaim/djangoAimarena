from datetime import datetime, timedelta

from django import template
from django.db.models import Q
from forum.models import Post, topic, Comment, subtopic, subtopiclatestposts, Notification
from forum.views import returns
from nonmotiongame.models import User_Info

register = template.Library()


@register.simple_tag
def newposts(subtopicid, iduser):
    x = subtopiclatestposts.objects.filter(subtopicnew=subtopicid, user=iduser, is_read=False)
    print("notify")
    print(x)
    return x


@register.simple_tag
def countcommments(pk):
    commentc = Comment.objects.filter(post_id=pk, deleted=False).count()

    return commentc


@register.simple_tag
def countpostsforusers(pk):
    print(pk)
    countposts = Post.objects.filter(author_id=pk).count()
    print('countposts')
    print(countposts)
    return countposts


@register.simple_tag
def countpointsforusers(pk):
    print(pk)
    userexists = User_Info.objects.filter(User_ID_id=pk)
    if userexists:
        countpoints = User_Info.objects.values_list('forumpoints', flat=True).get(User_ID_id=pk)
        print('countpoints')
        print(countpoints)
        return countpoints


@register.simple_tag
def checksubtopicvisiblity(subtopicslug):
    print("subtopicslug")
    print(subtopicslug)
    x = subtopic.objects.filter(Q(slug=subtopicslug) &
                                Q(subtopic_visible=False)
                                )
    print(x)
    if x.count():
        print("yes")
        return True
    else:
        return False


@register.simple_tag
def checksubtopicdeleted(subtopicslug):
    print("subtopicslug")
    print(subtopicslug)
    x = subtopic.objects.filter(Q(slug=subtopicslug) &
                                Q(subtopic_deleted=True)
                                )
    print(x)
    if x.count():
        print("yes")
        return True
    else:
        return False


@register.simple_tag
def countnotification(userid):
    count_notifications = Notification.objects.filter(user=userid, is_read=False).count()
    print("count_notifications")
    print(count_notifications)
    return count_notifications


@register.simple_tag
def notdeletedreplies(replyid):
    x = Comment.objects.filter(Q(id=replyid) &
                               Q(deleted=True)).exclude(reply_id=None)

    if x.count() > 0:
        return True
    else:
        return False


@register.simple_tag
def countviews(postid):
    x = Post.objects.values_list('post_views', flat=True).get(id=postid)
    return x


register.filter('countviews', countviews)
register.filter('countnotification', countnotification)
register.filter('countcommments', countcommments)
register.filter('newposts', newposts)
register.filter('countpostsforusers', countpostsforusers)
register.filter('checksubtopicvisiblity', checksubtopicvisiblity)
register.filter('checksubtopicdeleted', checksubtopicdeleted)
register.filter('notdeletedreplies', notdeletedreplies)
register.filter('countpointsforusers', countpointsforusers)
