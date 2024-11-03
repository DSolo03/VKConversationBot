import vk_api as VK
from storage import Storage
from vk_api.bot_longpoll import VkBotLongPoll,VkBotEventType

Storage=Storage()

vk_s=VK.VkApi(token=Storage("botToken"))
vk_u=VK.VkApi(token=Storage("userToken"))
Longpoll=VkBotLongPoll(vk_s,201340515)
API=vk_s.get_api()
APIu=vk_u.get_api()
newMessage=VkBotEventType.MESSAGE_NEW
 
