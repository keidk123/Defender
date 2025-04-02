import pygame
import random
import time  # إضافة مكتبة الوقت لعرض شاشة البداية

# تهيئة Pygame
pygame.init()

# تهيئة الصوت
pygame.mixer.init()
collision_sound = pygame.mixer.Sound("collision.wav")  # استبدل "collision.wav" بمسار ملف الصوت

# إعداد الشاشة
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Defender Game")

# الألوان
white = (255, 255, 255)
black = (0, 0, 0)

# تحميل الصور
try:
    player_img = pygame.image.load("player.png")  # استبدل "player.png" بمسار صورتك
    enemy_img = pygame.image.load("enemy.png")    # استبدل "enemy.png" بمسار صورتك
    bullet_img = pygame.image.load("bullet.png")   # استبدل "bullet.png" بمسار صورتك
    splash_img = pygame.image.load("splash.jpg")   # استبدل "splash.png" بمسار صورة البداية
    # التأكد من أن صورة البداية بحجم 300x300
    splash_img = pygame.transform.scale(splash_img, (300, 300))
except pygame.error:
    # إذا لم يتم العثور على صورة البداية، سننشئ صورة بديلة
    print("لم يتم العثور على إحدى الصور، سيتم استخدام صور بديلة.")
    # إنشاء صورة بديلة للبداية بحجم 300x300
    splash_img = pygame.Surface((300, 300))
    splash_img.fill(black)
    font = pygame.font.SysFont(None, 36)
    title_text = font.render("Defender Game", True, (255, 0, 0))
    splash_img.blit(title_text, (150 - title_text.get_width()//2, 150 - title_text.get_height()//2))

# إعداد اللاعب
player_rect = player_img.get_rect()
player_rect.x = width // 2 - player_rect.width // 2
player_rect.y = height - player_rect.height
player_speed = 5

# إعداد الأعداء
enemy_speed = 3
enemies = []

def create_enemy():
    enemy_rect = enemy_img.get_rect()
    enemy_rect.x = random.randint(0, width - enemy_rect.width)
    enemy_rect.y = 0
    enemies.append(enemy_rect)

# إعداد الطلقات
bullet_speed = 7
bullets = []

def fire_bullet():
    bullet_rect = bullet_img.get_rect()
    bullet_rect.x = player_rect.x + player_rect.width // 2 - bullet_rect.width // 2
    bullet_rect.y = player_rect.y
    bullets.append(bullet_rect)

# دالة لعرض شاشة البداية
def show_splash_screen(duration=2):
    start_time = time.time()
    running = True
    
    # حساب موقع صورة البداية في منتصف الشاشة
    splash_x = width // 2 - splash_img.get_width() // 2
    splash_y = height // 2 - splash_img.get_height() // 2
    
    while running and time.time() - start_time < duration:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            # إمكانية تخطي شاشة البداية بالضغط على أي مفتاح
            elif event.type == pygame.KEYDOWN:
                return True
        
        # تعبئة الشاشة باللون الأسود
        screen.fill(black)
        # عرض صورة البداية في المنتصف
        screen.blit(splash_img, (splash_x, splash_y))
        pygame.display.flip()
        
    return True

# عرض شاشة البداية لمدة ثانيتين
if not show_splash_screen(2):
    pygame.quit()
    exit()

# حلقة اللعبة
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                fire_bullet()
    
    # تحريك اللاعب
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_rect.x > 0:
        player_rect.x -= player_speed
    if keys[pygame.K_RIGHT] and player_rect.x < width - player_rect.width:
        player_rect.x += player_speed
        
    # تحريك الأعداء
    if random.randint(0, 100) < 2:
        create_enemy()
        
    for enemy_rect in enemies[:]:  # استخدام نسخة من القائمة لتجنب الأخطاء أثناء التكرار
        enemy_rect.y += enemy_speed
        if enemy_rect.y > height:
            enemies.remove(enemy_rect)
            
    # تحريك الطلقات
    for bullet_rect in bullets[:]:  # استخدام نسخة من القائمة لتجنب الأخطاء أثناء التكرار
        bullet_rect.y -= bullet_speed
        if bullet_rect.y < 0:
            bullets.remove(bullet_rect)
            
    # التحقق من التصادم
    for enemy_rect in enemies[:]:  # استخدام نسخة من القائمة لتجنب الأخطاء أثناء التكرار
        if player_rect.colliderect(enemy_rect):
            running = False
            
        for bullet_rect in bullets[:]:  # استخدام نسخة من القائمة لتجنب الأخطاء أثناء التكرار
            if enemy_rect.colliderect(bullet_rect):
                if enemy_rect in enemies:
                    enemies.remove(enemy_rect)
                if bullet_rect in bullets:
                    bullets.remove(bullet_rect)
                    collision_sound.play()
                break  # الخروج من الحلقة بعد إزالة العدو
                
    # الرسم
    screen.fill(white)
    screen.blit(player_img, player_rect)
    
    for enemy_rect in enemies:
        screen.blit(enemy_img, enemy_rect)
        
    for bullet_rect in bullets:
        screen.blit(bullet_img, bullet_rect)
        
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
