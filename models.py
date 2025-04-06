from tortoise.models import Model
from tortoise.fields import SmallIntField, IntField, BigIntField, FloatField, CharField, TextField, DatetimeField, BooleanField, JSONField
from urllib.parse import quote, unquote

class CommentsBaseModel(Model):
    '弹幕基类'
    time = DatetimeField()
    username = TextField()
    user_id = BigIntField()
    medal_name = CharField(max_length=10, null=True)
    medal_level = SmallIntField(null=True)
    guard_level = SmallIntField(default=0)
    text = TextField(null=True)
    superchat_price = FloatField(null=True)
    gift_name = TextField(null=True)
    gift_price = FloatField(null=True)
    gift_num = SmallIntField(null=True)

    class Meta:
        ordering = ['-time']

class AllComments(CommentsBaseModel):
    '所有弹幕, 但是好像实际上在API里完全没什么作用, 目前闲置'
    liver_uid = BigIntField()
    clip_id = CharField(max_length=35,null=True)

class Comments(CommentsBaseModel):
    '正常弹幕'
    clip_id = CharField(max_length=35)

    @classmethod
    async def add(self, **kwargs):
        '添加单条弹幕'
        res = await Comments.create(**kwargs)
        # res = await AllComments.create(**kwargs)

class OffComments(CommentsBaseModel):
    '下播弹幕'
    liver_uid = BigIntField()

    @classmethod
    async def add(self, **kwargs):
        '添加单条弹幕'
        # tortoise应该..有做防注入的吧(转码好麻烦啊)
        # kwargs['username'] = quote(kwargs['username']),
        # kwargs['text'] = quote(kwargs['text']),
        res = await OffComments.create(**kwargs)
        # res = await AllComments.create(**kwargs)

class Channels(Model):
    '房间列表'
    name = TextField()
    bilibili_uid = BigIntField()
    bilibili_live_room = BigIntField(primary_key=True)
    is_live = BooleanField()
    last_danmu = IntField()
    total_clips = IntField()
    total_danmu = IntField()
    face = TextField()
    hidden = BooleanField(null=True)
    archive = BooleanField(null=True)
    last_live = DatetimeField(null=True)

    class Meta:
        ordering = ['-last_live']
        indexes = ['bilibili_live_room', 'bilibili_uid']

class ClipInfo(Model):
    '直播场次列表'
    id = CharField(max_length=35, unique=True, primary_key=True)
    bilibili_uid = BigIntField()
    title = TextField(default="")
    start_time = DatetimeField()
    end_time = DatetimeField()
    cover = TextField(default="")
    danmu_density = FloatField(default=0)
    total_danmu = IntField(default=0)
    total_gift = FloatField(default=0)
    total_superchat = FloatField(default=0)
    total_reward = FloatField(default=0)
    highlights = JSONField(default=0)
    viewers = IntField(default=0)

    class Meta:
        ordering = ['-start_time']
        indexes = ['id']
