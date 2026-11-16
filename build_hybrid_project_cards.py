import os
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# -------------------------------------------------------------
# CONSTANTS & PALETTE (Matching User's 5-color theme + Telemetry)
# -------------------------------------------------------------
W, H = 1376, 768

C_BLACK   = (4, 21, 31)       # #04151F Rich black
C_SLATE   = (24, 58, 55)      # #183A37 Dark slate gray
C_WHEAT   = (239, 214, 172)   # #EFD6AC Wheat
C_ORANGE  = (196, 73, 0)      # #C44900 Mahogany / rust orange
C_PURPLE  = (67, 37, 52)      # #432534 Dark purple

# Additional high-contrast telemetry accents
C_GREEN   = (16, 185, 129)    # Emerald healthy
C_CYAN    = (6, 182, 212)     # Cyan telemetry
C_AMBER   = (245, 158, 11)    # Amber warning / event
C_RED     = (239, 68, 68)     # Red critical / error
C_WHITE   = (255, 255, 255)

# Fonts
FONT_DIR = r"C:\Windows\Fonts"
def get_font(name, size):
    try:
        return ImageFont.truetype(os.path.join(FONT_DIR, name), size)
    except Exception:
        try:
            return ImageFont.truetype(os.path.join(FONT_DIR, "arial.ttf"), size)
        except Exception:
            return ImageFont.load_default()

F_TITLE = get_font("arialbd.ttf", 26)
F_SUB   = get_font("consola.ttf", 13)
F_HEAD  = get_font("arialbd.ttf", 16)
F_BODY  = get_font("arial.ttf", 13)
F_BOLD  = get_font("arialbd.ttf", 13)
F_MONO  = get_font("consola.ttf", 12)
F_MONO_SM = get_font("consola.ttf", 10)
F_MONO_XS = get_font("consola.ttf", 9)
F_BADGE = get_font("arialbd.ttf", 11)

def draw_rounded_rect(draw, bbox, fill, outline=None, width=1, radius=8):
    draw.rounded_rectangle(bbox, radius=radius, fill=fill, outline=outline, width=width)

def draw_glow_rect(draw, bbox, glow_color, radius=8):
    # Draw soft outer glow
    x0, y0, x1, y1 = bbox
    for i in range(3, 0, -1):
        color = (*glow_color[:3], int(30 / i))
        draw.rounded_rectangle([x0 - i, y0 - i, x1 + i, y1 + i], radius=radius + i, outline=color, width=1)

def draw_pill(draw, x, y, text, bg_color, text_color, font=F_BADGE, dot_color=None, border_color=None):
    text_bbox = font.getbbox(text)
    tw = text_bbox[2] - text_bbox[0]
    th = text_bbox[3] - text_bbox[1]
    
    pad_x = 10
    pad_y = 5
    dot_space = 14 if dot_color else 0
    w = tw + pad_x * 2 + dot_space
    h = th + pad_y * 2
    
    bbox = [x, y, x + w, y + h]
    draw.rounded_rectangle(bbox, radius=h//2, fill=bg_color, outline=border_color or bg_color, width=1)
    
    tx = x + pad_x
    if dot_color:
        dot_r = 3.5
        draw.ellipse([tx, y + h//2 - dot_r, tx + dot_r*2, y + h//2 + dot_r], fill=dot_color)
        tx += dot_space
        
    draw.text((tx, y + (h - th)//2 - 1), text, fill=text_color, font=font)
    return w

def draw_connector(draw, p1, p2, color=C_ORANGE, width=2, dashed=False, label=None):
    x1, y1 = p1
    x2, y2 = p2
    
    if x1 == x2 or y1 == y2:
        draw.line([p1, p2], fill=color, width=width)
    else:
        # 90 degree elbow connector
        mid_x = (x1 + x2) // 2
        draw.line([(x1, y1), (mid_x, y1)], fill=color, width=width)
        draw.line([(mid_x, y1), (mid_x, y2)], fill=color, width=width)
        draw.line([(mid_x, y2), (x2, y2)], fill=color, width=width)
        
    # Draw small terminal arrow or dot at p2
    draw.ellipse([x2 - 3, y2 - 3, x2 + 3, y2 + 3], fill=color)
    
    if label:
        mid = ((x1 + x2) // 2, (y1 + y2) // 2)
        tw = F_MONO_XS.getbbox(label)[2] - F_MONO_XS.getbbox(label)[0]
        draw.rounded_rectangle([mid[0] - tw//2 - 4, mid[1] - 8, mid[0] + tw//2 + 4, mid[1] + 8], radius=4, fill=C_BLACK, outline=color, width=1)
        draw.text((mid[0] - tw//2, mid[1] - 6), label, fill=C_WHEAT, font=F_MONO_XS)

def create_base_canvas(grid_color=(24, 58, 55), bg_glow_pos=(W//2, H//2), glow_color=(196, 73, 0)):
    im = Image.new('RGB', (W, H), C_BLACK)
    draw = ImageDraw.Draw(im)
    
    # Subtle vertical gradient
    for y in range(H):
        factor = y / H
        r = int(C_BLACK[0] + (C_SLATE[0] * 0.25) * factor)
        g = int(C_BLACK[1] + (C_SLATE[1] * 0.25) * factor)
        b = int(C_BLACK[2] + (C_SLATE[2] * 0.25) * factor)
        draw.line([(0, y), (W, y)], fill=(r, g, b))
        
    # Subtle isometric / technical grid
    grid_im = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    gdraw = ImageDraw.Draw(grid_im)
    spacing = 48
    for x in range(0, W, spacing):
        gdraw.line([(x, 0), (x, H)], fill=(*grid_color, 35))
    for y in range(0, H, spacing):
        gdraw.line([(0, y), (W, y)], fill=(*grid_color, 35))
        
    # Center ambient glow
    gx, gy = bg_glow_pos
    glow_overlay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow_overlay)
    glow_draw.ellipse([gx - 350, gy - 250, gx + 350, gy + 250], fill=(*glow_color, 25))
    glow_overlay = glow_overlay.filter(ImageFilter.GaussianBlur(80))
    
    im.paste(grid_im, (0, 0), grid_im)
    im.paste(glow_overlay, (0, 0), glow_overlay)
    return im

print('Base generator utilities compiled.')
# =============================================================
# CARD 1: KUBEHEAL — AUTONOMOUS SRE OPERATOR
# =============================================================
def generate_kubeheal_card(out_path):
    im = create_base_canvas(grid_color=C_SLATE, bg_glow_pos=(W//2, 380), glow_color=C_ORANGE)
    draw = ImageDraw.Draw(im)
    
    # ---------------- HUD TOP BAR ----------------
    draw.rectangle([0, 0, W, 58], fill=(6, 26, 36))
    draw.line([(0, 58), (W, 58)], fill=C_SLATE, width=1)
    
    # Title & Subtitle
    draw.text((28, 14), "KUBEHEAL", fill=C_WHEAT, font=F_TITLE)
    draw.text((185, 23), "// AUTONOMOUS KUBERNETES SRE OPERATOR", fill=C_ORANGE, font=F_SUB)
    
    # Right-aligned Status Badges
    rx = W - 28
    rx -= draw_pill(draw, rx - 165, 14, "OPERATOR: ACTIVE", C_BLACK, C_WHEAT, F_BADGE, dot_color=C_GREEN, border_color=C_SLATE)
    rx -= 12
    rx -= draw_pill(draw, rx - 145, 14, "GIT-OPS: SYNCED", C_BLACK, C_WHEAT, F_BADGE, dot_color=C_CYAN, border_color=C_SLATE)
    rx -= 12
    draw_pill(draw, rx - 180, 14, "AWS EKS (ap-south-1)", C_BLACK, (200, 200, 200), F_BADGE, border_color=C_SLATE)
    
    # ---------------- MAIN CONTENT AREA (y=74 to 684) ----------------
    
    # Panel 1: Amazon EKS Production Cluster (Left, w=440)
    p1_box = [28, 76, 468, 680]
    draw.rounded_rectangle(p1_box, radius=12, fill=(8, 28, 38), outline=C_SLATE, width=2)
    # Header tab
    draw.rounded_rectangle([28, 76, 468, 114], radius=12, fill=(14, 44, 52), outline=C_SLATE, width=1)
    draw.text((44, 86), "AMAZON EKS CLUSTER WORKLOADS", fill=C_WHEAT, font=F_HEAD)
    draw.text((360, 89), "VPC: 10.0.0.0/16", fill=C_CYAN, font=F_MONO_SM)
    
    # Ingress Controller
    ing_box = [46, 128, 450, 190]
    draw.rounded_rectangle(ing_box, radius=8, fill=(12, 34, 44), outline=C_CYAN, width=1)
    draw.text((60, 138), "AWS ALB  ->  NGINX Ingress Controller", fill=C_WHEAT, font=F_BOLD)
    draw.text((60, 160), "TLS Termination  *  Rate Limit  *  Target Group (Port: 3000)", fill=(160, 185, 195), font=F_MONO_SM)
    
    # Worker Node 01 (AZ-A)
    wn1_box = [46, 206, 450, 420]
    draw.rounded_rectangle(wn1_box, radius=8, fill=(10, 30, 40), outline=C_SLATE, width=1)
    draw.text((58, 218), "WORKER NODE 01 (EKS Node Group AZ-A)", fill=C_WHEAT, font=F_BOLD)
    draw.text((350, 220), "IP: 10.0.101.4", fill=(140, 160, 170), font=F_MONO_SM)
    
    # Pods inside Node 01
    # Pod A (Normal)
    draw.rounded_rectangle([60, 246, 436, 300], radius=6, fill=(8, 24, 32), outline=(20, 60, 60), width=1)
    draw.text((72, 255), "pod/flight-search-6b8f", fill=C_WHEAT, font=F_MONO)
    draw.text((72, 275), "Containers: 2/2  *  Restarts: 0  *  Memory: 210MiB", fill=(130, 160, 170), font=F_MONO_SM)
    draw_pill(draw, 340, 256, "RUNNING", (16, 185, 129, 40), C_GREEN, F_MONO_XS, dot_color=C_GREEN, border_color=C_GREEN)
    
    # Pod B (CrashLoopBackOff Incident!)
    draw.rounded_rectangle([60, 314, 436, 404], radius=6, fill=(35, 18, 22), outline=C_RED, width=1)
    draw.text((72, 324), "pod/booking-service-84d2", fill=(255, 200, 200), font=F_MONO)
    draw.text((72, 344), "CRITICAL: ExitCode 137 (OOMKilled)  *  Restart: 4x", fill=C_RED, font=F_MONO_SM)
    draw.text((72, 364), "Kubelet: Back-off restarting failed container", fill=(220, 140, 140), font=F_MONO_SM)
    draw_pill(draw, 276, 324, "CRASHLOOPBACKOFF", (239, 68, 68, 40), C_RED, F_MONO_XS, dot_color=C_RED, border_color=C_RED)
    
    # Worker Node 02 (AZ-B)
    wn2_box = [46, 434, 450, 540]
    draw.rounded_rectangle(wn2_box, radius=8, fill=(10, 30, 40), outline=C_SLATE, width=1)
    draw.text((58, 446), "WORKER NODE 02 (EKS Node Group AZ-B)", fill=C_WHEAT, font=F_BOLD)
    draw.text((350, 448), "IP: 10.0.102.8", fill=(140, 160, 170), font=F_MONO_SM)
    
    draw.rounded_rectangle([60, 472, 436, 526], radius=6, fill=(8, 24, 32), outline=(20, 60, 60), width=1)
    draw.text((72, 482), "pod/payment-service-5c91", fill=C_WHEAT, font=F_MONO)
    draw.text((72, 502), "Containers: 1/1  *  Restarts: 0  *  Memory: 185MiB", fill=(130, 160, 170), font=F_MONO_SM)
    draw_pill(draw, 340, 483, "RUNNING", (16, 185, 129, 40), C_GREEN, F_MONO_XS, dot_color=C_GREEN, border_color=C_GREEN)
    
    # Data Layer Box
    draw.rounded_rectangle([46, 554, 450, 664], radius=8, fill=(12, 36, 46), outline=C_SLATE, width=1)
    draw.text((58, 566), "STATE PERSISTENCE & AUDIT LOGS", fill=C_WHEAT, font=F_BOLD)
    draw.text((60, 592), "- Amazon RDS (PostgreSQL Multi-AZ Primary)", fill=(160, 190, 200), font=F_MONO_SM)
    draw.text((60, 614), "- Amazon S3 (Immutable Incident Forensics & RCA)", fill=(160, 190, 200), font=F_MONO_SM)
    draw.text((60, 636), "- Amazon SQS (Incident Queue & Notification DLQ)", fill=(160, 190, 200), font=F_MONO_SM)

    # Panel 2: KubeHeal Core Operator Engine (Center, w=460)
    p2_box = [484, 76, 944, 680]
    draw.rounded_rectangle(p2_box, radius=12, fill=(12, 32, 42), outline=C_ORANGE, width=2)
    # Header tab
    draw.rounded_rectangle([484, 76, 944, 114], radius=12, fill=(24, 48, 54), outline=C_ORANGE, width=1)
    draw.text((504, 86), "KUBEHEAL CONTROLLER RECONCILIATION LOOP", fill=C_WHEAT, font=F_HEAD)
    draw_pill(draw, 840, 83, "DAEMON v2.4", C_BLACK, C_ORANGE, F_MONO_XS, border_color=C_ORANGE)
    
    # 4-Stage State Machine Cards inside Center Panel
    stages = [
        ("01. EVENT DETECTION", "Kubernetes Watch API stream detects CrashLoopBackOff", "Captured ExitCode 137 from booking-service pod", C_RED),
        ("02. ROOT CAUSE ANALYSIS (RCA)", "FastAPI Engine inspects Pod Specs & Container Logs", "Diagnosis: Memory request (256MiB) exceeded during peak burst", C_AMBER),
        ("03. AUTOMATED REMEDIATION", "Self-Healing Policy Trigger: Dynamic Resource Tuning", "Action: Executed rolling patch memory.limits -> 512MiB", C_CYAN),
        ("04. RECONCILIATION VERIFIED", "Pod successfully restarted & passed Readiness Probe", "Pod Restored: booking-service (2/2) Running, 0 errors", C_GREEN),
    ]
    
    sy = 132
    for title, desc1, desc2, st_color in stages:
        s_box = [504, sy, 924, sy + 104]
        draw.rounded_rectangle(s_box, radius=8, fill=(8, 22, 30), outline=st_color, width=1)
        draw.text((518, sy + 12), title, fill=st_color, font=F_BOLD)
        draw.text((518, sy + 38), desc1, fill=C_WHEAT, font=F_BODY)
        draw.text((518, sy + 62), desc2, fill=(140, 170, 180), font=F_MONO_SM)
        
        # Indicator badge
        draw_pill(draw, 820, sy + 10, "PROCESSED", C_BLACK, st_color, F_MONO_XS, dot_color=st_color, border_color=st_color)
        
        # Draw connector arrow down to next stage
        if title != stages[-1][0]:
            draw.line([(714, sy + 104), (714, sy + 122)], fill=st_color, width=2)
            draw.polygon([(710, sy + 118), (718, sy + 118), (714, sy + 124)], fill=st_color)
        sy += 124
        
    # Healed Pod Result Badge in Center
    draw.rounded_rectangle([504, sy, 924, sy + 70], radius=8, fill=(10, 40, 30), outline=C_GREEN, width=2)
    draw.text((518, sy + 14), "OUTCOME: ZERO SRE HUMAN INTERVENTION", fill=C_GREEN, font=F_BOLD)
    draw.text((518, sy + 38), "Pod healthy in 4.2s  *  Audit recorded to S3  *  Slack alert dispatched", fill=C_WHEAT, font=F_MONO_SM)

    # Panel 3: GitOps Sync & Telemetry (Right, w=384)
    p3_box = [960, 76, W - 28, 680]
    draw.rounded_rectangle(p3_box, radius=12, fill=(8, 28, 38), outline=C_SLATE, width=2)
    # Header tab
    draw.rounded_rectangle([960, 76, W - 28, 114], radius=12, fill=(14, 44, 52), outline=C_SLATE, width=1)
    draw.text((980, 86), "GITOPS & SRE OBSERVABILITY", fill=C_WHEAT, font=F_HEAD)
    
    # ArgoCD GitOps Sync Box
    argo_box = [978, 128, W - 46, 280]
    draw.rounded_rectangle(argo_box, radius=8, fill=(10, 32, 42), outline=C_CYAN, width=1)
    draw.text((992, 140), "Argo CD GitOps Synchronization", fill=C_WHEAT, font=F_BOLD)
    draw.text((992, 168), "Repo: github.com/NikhilReddy9110/KubeHeal", fill=(140, 180, 200), font=F_MONO_SM)
    draw.text((992, 192), "Target: Helm 3 ApplicationSets", fill=(140, 180, 200), font=F_MONO_SM)
    draw.text((992, 216), "Sync Status: Synced (Self-Heal Active)", fill=C_GREEN, font=F_MONO_SM)
    draw.text((992, 240), "Cluster Drift: 0.00% (Auto-Reconciled)", fill=C_CYAN, font=F_MONO_SM)
    
    # Prometheus Telemetry Box
    prom_box = [978, 296, W - 46, 480]
    draw.rounded_rectangle(prom_box, radius=8, fill=(10, 32, 42), outline=C_SLATE, width=1)
    draw.text((992, 308), "Prometheus & CloudWatch Metrics", fill=C_WHEAT, font=F_BOLD)
    
    # Mini Metrics Cards
    metrics = [
        ("POD AVAILABILITY", "99.98%", C_GREEN),
        ("MEAN TIME TO REPAIR", "4.2 sec", C_CYAN),
        ("AUTO-HEAL ACTIONS", "14 / 14", C_ORANGE),
        ("DRIFT RECOVERY", "100%", C_WHEAT)
    ]
    my = 340
    for label, val, m_col in metrics:
        draw.rounded_rectangle([992, my, W - 64, my + 30], radius=4, fill=(6, 20, 28), outline=(20, 50, 60), width=1)
        draw.text((1004, my + 8), label, fill=(150, 175, 185), font=F_MONO_SM)
        draw.text((1220, my + 6), val, fill=m_col, font=F_BOLD)
        my += 33
        
    # SRE Tech Badges Strip
    badges_box = [978, 496, W - 46, 664]
    draw.rounded_rectangle(badges_box, radius=8, fill=(10, 30, 40), outline=C_SLATE, width=1)
    draw.text((992, 508), "VERIFIED SRE TECH STACK", fill=C_WHEAT, font=F_BOLD)
    
    stack = [
        ("Kubernetes", C_CYAN),
        ("Python 3.11", C_WHEAT),
        ("FastAPI", C_GREEN),
        ("Helm 3", C_CYAN),
        ("Argo CD", C_ORANGE),
        ("Terraform", C_PURPLE),
        ("Prometheus", C_ORANGE),
        ("AWS EKS", C_AMBER)
    ]
    bx, by = 992, 538
    for st_name, st_col in stack:
        bw = draw_pill(draw, bx, by, st_name, C_BLACK, st_col, F_MONO_SM, dot_color=st_col, border_color=C_SLATE)
        bx += bw + 8
        if bx > W - 140:
            bx = 992
            by += 32
            
    # Connectors between panels
    # Connector from CrashLoopBackOff Pod -> Operator Panel
    draw_connector(draw, (436, 359), (504, 184), color=C_RED, width=2, label="INCIDENT DETECTED")
    # Connector from Operator Panel -> GitOps Panel
    draw_connector(draw, (924, 444), (978, 204), color=C_CYAN, width=2, label="HELM ROLLOUT")

    # ---------------- BOTTOM TERMINAL HUD (y=694 to 756) ----------------
    draw.rounded_rectangle([28, 694, W - 28, 754], radius=8, fill=(6, 20, 28), outline=C_SLATE, width=1)
    draw.text((44, 706), "DAEMON LOG: [INFO] kubeheal-operator watching 48 pods across namespace:default | reconciliation complete in 4200ms", fill=C_GREEN, font=F_MONO)
    draw.text((44, 728), "STATUS AUDIT: pod/booking-service-84d2 healed | memory limit adjusted to 512MiB | 0 downtime observed", fill=(160, 180, 190), font=F_MONO_SM)

    im.save(out_path, quality=95)
    print(f"Successfully generated {out_path}")

print('Card 1 generator compiled.')
# =============================================================
# CARD 2: FLIGHT BOOKING MICROSERVICES
# =============================================================
def generate_flight_card(out_path):
    im = create_base_canvas(grid_color=C_SLATE, bg_glow_pos=(W//2, 380), glow_color=C_PURPLE)
    draw = ImageDraw.Draw(im)
    
    # ---------------- HUD TOP BAR ----------------
    draw.rectangle([0, 0, W, 58], fill=(6, 26, 36))
    draw.line([(0, 58), (W, 58)], fill=C_SLATE, width=1)
    
    draw.text((28, 14), "FLIGHT BOOKING PLATFORM", fill=C_WHEAT, font=F_TITLE)
    draw.text((430, 23), "// EVENT-DRIVEN MICROSERVICES & KAFKA STREAMING", fill=C_ORANGE, font=F_SUB)
    
    rx = W - 28
    rx -= draw_pill(draw, rx - 145, 14, "THROUGHPUT: 12.5k TPS", C_BLACK, C_GREEN, F_BADGE, dot_color=C_GREEN, border_color=C_SLATE)
    rx -= 12
    rx -= draw_pill(draw, rx - 160, 14, "KAFKA: 4 TOPICS SYNCED", C_BLACK, C_CYAN, F_BADGE, dot_color=C_CYAN, border_color=C_SLATE)
    rx -= 12
    draw_pill(draw, rx - 165, 14, "TERRAFORM AWS VPC", C_BLACK, (200, 200, 200), F_BADGE, border_color=C_SLATE)
    
    # ---------------- MAIN CONTENT AREA (y=76 to 680) ----------------
    
    # Tier 1: Ingress & API Gateway (Top wide box, y=76 to 186)
    t1_box = [28, 76, W - 28, 186]
    draw.rounded_rectangle(t1_box, radius=12, fill=(8, 28, 38), outline=C_SLATE, width=2)
    # Header tab
    draw.rounded_rectangle([28, 76, W - 28, 110], radius=12, fill=(14, 44, 52), outline=C_SLATE, width=1)
    draw.text((44, 84), "EDGE INGRESS & API GATEWAY TIER", fill=C_WHEAT, font=F_HEAD)
    draw.text((360, 87), "AWS Cloud ap-south-1 (Public Subnet)", fill=C_CYAN, font=F_MONO_SM)
    
    # 3 Ingress blocks
    gw_w = (W - 56 - 40) // 3
    # Block 1: Route53 & WAF
    draw.rounded_rectangle([44, 120, 44 + gw_w, 174], radius=6, fill=(12, 34, 44), outline=C_SLATE, width=1)
    draw.text((56, 128), "AWS Route 53 + AWS WAF", fill=C_WHEAT, font=F_BOLD)
    draw.text((56, 150), "DDoS Protection  *  SSL/TLS Termination", fill=(150, 180, 190), font=F_MONO_SM)
    
    # Block 2: ALB
    draw.rounded_rectangle([44 + gw_w + 20, 120, 44 + gw_w*2 + 20, 174], radius=6, fill=(12, 34, 44), outline=C_CYAN, width=1)
    draw.text((56 + gw_w + 20, 128), "Application Load Balancer (ALB)", fill=C_WHEAT, font=F_BOLD)
    draw.text((56 + gw_w + 20, 150), "Path Routing  *  Health Probes  *  Multi-AZ", fill=(150, 180, 190), font=F_MONO_SM)
    
    # Block 3: Spring Cloud Gateway
    draw.rounded_rectangle([44 + (gw_w + 20)*2, 120, W - 44, 174], radius=6, fill=(12, 34, 44), outline=C_ORANGE, width=1)
    draw.text((56 + (gw_w + 20)*2, 128), "Spring Cloud API Gateway (:8080)", fill=C_WHEAT, font=F_BOLD)
    draw.text((56 + (gw_w + 20)*2, 150), "JWT Auth Filter  *  Rate Limiting  *  CORS", fill=(150, 180, 190), font=F_MONO_SM)

    # Tier 2: Microservices Mesh (4 Independent Services, y=202 to 392)
    t2_box = [28, 202, W - 28, 396]
    draw.rounded_rectangle(t2_box, radius=12, fill=(8, 26, 36), outline=C_ORANGE, width=2)
    # Header tab
    draw.rounded_rectangle([28, 202, W - 28, 236], radius=12, fill=(24, 46, 52), outline=C_ORANGE, width=1)
    draw.text((44, 210), "SPRING BOOT MICROSERVICES MESH (Containerized on Amazon EKS)", fill=C_WHEAT, font=F_HEAD)
    draw_pill(draw, W - 180, 208, "AUTOSCALING HPA", C_BLACK, C_GREEN, F_MONO_XS, dot_color=C_GREEN, border_color=C_SLATE)
    
    svc_w = (W - 56 - 60) // 4
    services = [
        ("Flight Search Service", "Port: 8081  *  REST/JSON", "Route & Schedule Indexer", "Redis Cache Query (<2ms)", C_CYAN),
        ("Booking Coordinator", "Port: 8082  *  Saga Pattern", "Seat Lock & PNR Engine", "2-Phase Commit Orchestrator", C_ORANGE),
        ("Payment Gateway Svc", "Port: 8083  *  Stripe API", "Idempotent Txn Engine", "PCI-DSS Vault Tokenized", C_AMBER),
        ("Notification Broker", "Port: 8084  *  AWS SNS/SES", "Boarding Pass PDF Gen", "Async SMS & Email Dispatch", C_GREEN)
    ]
    
    sx = 44
    for s_title, s_port, s_f1, s_f2, s_col in services:
        s_box = [sx, 248, sx + svc_w, 384]
        draw.rounded_rectangle(s_box, radius=8, fill=(10, 30, 40), outline=s_col, width=1)
        draw.text((sx + 14, 258), s_title, fill=C_WHEAT, font=F_BOLD)
        draw.text((sx + 14, 280), s_port, fill=s_col, font=F_MONO_SM)
        
        # Details
        draw.text((sx + 14, 308), f"- {s_f1}", fill=(180, 200, 210), font=F_MONO_SM)
        draw.text((sx + 14, 330), f"- {s_f2}", fill=(180, 200, 210), font=F_MONO_SM)
        
        # Status Pill
        draw_pill(draw, sx + 14, 354, "HEALTH: 100%", (16, 185, 129, 30), C_GREEN, F_MONO_XS, dot_color=C_GREEN, border_color=C_GREEN)
        
        # Connectors down to Kafka bus
        cx = sx + svc_w // 2
        draw.line([(cx, 384), (cx, 412)], fill=s_col, width=2)
        draw.polygon([(cx - 4, 408), (cx + 4, 408), (cx, 414)], fill=s_col)
        
        sx += svc_w + 20

    # Tier 3: Apache Kafka Distributed Event Spine (y=412 to 506)
    k_box = [28, 412, W - 28, 506]
    draw.rounded_rectangle(k_box, radius=12, fill=(14, 28, 40), outline=C_CYAN, width=2)
    # Header strip inside
    draw.rounded_rectangle([28, 412, W - 28, 442], radius=12, fill=(18, 42, 54), outline=C_CYAN, width=1)
    draw.text((44, 420), "APACHE KAFKA CLUSTER (Distributed Event Streaming Backbone)", fill=C_CYAN, font=F_HEAD)
    draw.text((640, 423), "Cluster: 3 Brokers (Multi-AZ)  *  Replication Factor: 3  *  Min In-Sync: 2", fill=C_WHEAT, font=F_MONO_SM)
    
    # 4 Kafka Topic Cards
    top_w = (W - 56 - 60) // 4
    topics = [
        ("topic: flight.search.events", "Partitions: 6  *  TTL: 24h", "Consumer: SearchAnalyticsGroup"),
        ("topic: booking.initiated", "Partitions: 8  *  Compacted", "Consumer: BookingSagaWorker"),
        ("topic: payment.completed", "Partitions: 8  *  Strict FIFO", "Consumer: TicketIssuingEngine"),
        ("topic: notification.dispatch", "Partitions: 4  *  At-least-once", "Consumer: EmailNotificationGroup")
    ]
    tx = 44
    for t_name, t_meta, t_cons in topics:
        t_box = [tx, 452, tx + top_w, 498]
        draw.rounded_rectangle(t_box, radius=6, fill=(8, 22, 32), outline=C_SLATE, width=1)
        draw.text((tx + 10, 458), t_name, fill=C_WHEAT, font=F_MONO_SM)
        draw.text((tx + 10, 474), t_meta, fill=(140, 175, 185), font=F_MONO_XS)
        tx += top_w + 20

    # Tier 4: Distributed Data & Caching Tier (y=522 to 680)
    # Left: Redis Cache (w=420)
    r_box = [28, 522, 450, 680]
    draw.rounded_rectangle(r_box, radius=12, fill=(8, 28, 38), outline=C_SLATE, width=2)
    draw.rounded_rectangle([28, 522, 450, 558], radius=12, fill=(14, 44, 52), outline=C_SLATE, width=1)
    draw.text((44, 532), "REDIS IN-MEMORY CACHE CLUSTER", fill=C_WHEAT, font=F_HEAD)
    
    draw.text((44, 570), "- Redis Sentinel 3-Node Cluster (High Availability)", fill=(160, 190, 200), font=F_MONO_SM)
    draw.text((44, 594), "- Seat Reservation Lock (TTL: 15-min auto expire)", fill=C_CYAN, font=F_MONO_SM)
    draw.text((44, 618), "- Cached Flight Routes & Price Schedule (<1ms)", fill=(160, 190, 200), font=F_MONO_SM)
    draw.text((44, 642), "- Distributed Session State & Token Store", fill=(160, 190, 200), font=F_MONO_SM)

    # Center: Amazon RDS PostgreSQL (w=480)
    db_box = [468, 522, 940, 680]
    draw.rounded_rectangle(db_box, radius=12, fill=(8, 28, 38), outline=C_SLATE, width=2)
    draw.rounded_rectangle([468, 522, 940, 558], radius=12, fill=(14, 44, 52), outline=C_SLATE, width=1)
    draw.text((484, 532), "AMAZON RDS POSTGRESQL (MULTI-AZ)", fill=C_WHEAT, font=F_HEAD)
    
    draw.text((484, 570), "- Multi-AZ Primary + Asynchronous Read Replica", fill=(160, 190, 200), font=F_MONO_SM)
    draw.text((484, 594), "- ACID Compliant Booking Ledger & Ticket Records", fill=C_ORANGE, font=F_MONO_SM)
    draw.text((484, 618), "- Connection Pooling via HikariCP (Max 80 Conns)", fill=(160, 190, 200), font=F_MONO_SM)
    draw.text((484, 642), "- Automated Point-in-time Recovery & EBS Snapshots", fill=(160, 190, 200), font=F_MONO_SM)

    # Right: Resilience & SRE (w=408)
    sre_box = [958, 522, W - 28, 680]
    draw.rounded_rectangle(sre_box, radius=12, fill=(8, 28, 38), outline=C_SLATE, width=2)
    draw.rounded_rectangle([958, 522, W - 28, 558], radius=12, fill=(14, 44, 52), outline=C_SLATE, width=1)
    draw.text((974, 532), "RESILIENCE & RECOVERY TIER", fill=C_WHEAT, font=F_HEAD)
    
    draw.text((974, 570), "- Resilience4j Circuit Breaker (Timeout: 500ms)", fill=(160, 190, 200), font=F_MONO_SM)
    draw.text((974, 594), "- Dead Letter Queue (SQS) for Failed Notifications", fill=C_RED, font=F_MONO_SM)
    draw.text((974, 618), "- OpenTelemetry & Zipkin Distributed Tracing", fill=C_GREEN, font=F_MONO_SM)
    draw.text((974, 642), "- Zero Split-Brain Guaranteed via Kafka Offsets", fill=(160, 190, 200), font=F_MONO_SM)

    # ---------------- BOTTOM TERMINAL HUD (y=694 to 754) ----------------
    draw.rounded_rectangle([28, 694, W - 28, 754], radius=8, fill=(6, 20, 28), outline=C_SLATE, width=1)
    draw.text((44, 706), "TRANSACTION LOG: [SAGA_2PC] Booking Txn FB-88402 SUCCESS | Kafka msg ack: 4/4 brokers | Redis seat locked in 1.4ms", fill=C_GREEN, font=F_MONO)
    draw.text((44, 728), "CLUSTER HEALTH: 4 Microservices Active | RDS Replication Lag: 0ms | AWS EKS HPA pods auto-scaled from 2 -> 6", fill=(160, 180, 190), font=F_MONO_SM)

    im.save(out_path, quality=95)
    print(f"Successfully generated {out_path}")

print('Card 2 generator compiled.')
# =============================================================
# CARD 3: USER MANAGEMENT SYSTEM
# =============================================================
def generate_user_card(out_path):
    im = create_base_canvas(grid_color=C_SLATE, bg_glow_pos=(W//2, 380), glow_color=C_ORANGE)
    draw = ImageDraw.Draw(im)
    
    # ---------------- HUD TOP BAR ----------------
    draw.rectangle([0, 0, W, 58], fill=(6, 26, 36))
    draw.line([(0, 58), (W, 58)], fill=C_SLATE, width=1)
    
    draw.text((28, 14), "USER MANAGEMENT SYSTEM", fill=C_WHEAT, font=F_TITLE)
    draw.text((435, 23), "// ENTERPRISE IAM, SPRING SECURITY 6 & RBAC", fill=C_ORANGE, font=F_SUB)
    
    rx = W - 28
    rx -= draw_pill(draw, rx - 165, 14, "AUTH: JWT (RSA-256)", C_BLACK, C_GREEN, F_BADGE, dot_color=C_GREEN, border_color=C_SLATE)
    rx -= 12
    rx -= draw_pill(draw, rx - 160, 14, "BCRYPT 12-ROUNDS", C_BLACK, C_CYAN, F_BADGE, dot_color=C_CYAN, border_color=C_SLATE)
    rx -= 12
    draw_pill(draw, rx - 165, 14, "SPRING BOOT 3.2", C_BLACK, (200, 200, 200), F_BADGE, border_color=C_SLATE)
    
    # ---------------- MAIN CONTENT AREA (y=76 to 680) ----------------
    
    # Panel 1: Spring Security 6 Authentication Pipeline (Left, w=510)
    p1_box = [28, 76, 538, 680]
    draw.rounded_rectangle(p1_box, radius=12, fill=(8, 28, 38), outline=C_ORANGE, width=2)
    # Header tab
    draw.rounded_rectangle([28, 76, 538, 114], radius=12, fill=(24, 46, 54), outline=C_ORANGE, width=1)
    draw.text((44, 86), "SPRING SECURITY 6 AUTHENTICATION PIPELINE", fill=C_WHEAT, font=F_HEAD)
    draw_pill(draw, 430, 83, "ZERO-TRUST", C_BLACK, C_ORANGE, F_MONO_XS, border_color=C_ORANGE)
    
    pipe_steps = [
        ("01. INBOUND REQUEST", "HTTPS 443 /api/v1/auth/** or protected resource", "Extract Bearer Token header / X-Forwarded-For", C_CYAN),
        ("02. CORS & CSRF FILTER", "Strict Origin Whitelist & Stateless CSRF Ignore", "SecurityFilterChain: SessionCreationPolicy.STATELESS", (160, 190, 200)),
        ("03. JWT AUTH FILTER", "Parse Claims: sub, roles, iat, exp, jti", "Verify RSA-256 Signature & Check Redis Blacklist", C_GREEN),
        ("04. DAO AUTH PROVIDER", "Retrieve UserDetails via UsernamePasswordToken", "Compare credentials using BCrypt (12-rounds salt)", C_AMBER),
        ("05. RBAC EVALUATION", "Method-level: @PreAuthorize(\"hasRole('ADMIN')\")", "GrantedAuthorities: ROLE_ADMIN, ROLE_SRE, ROLE_USER", C_ORANGE),
        ("06. SECURITY CONTEXT", "SecurityContextHolder.getContext().setAuthentication()", "ThreadLocal principal established for controller dispatch", C_GREEN)
    ]
    
    py = 126
    for step_title, s_line1, s_line2, s_col in pipe_steps:
        s_box = [44, py, 522, py + 80]
        draw.rounded_rectangle(s_box, radius=6, fill=(10, 28, 38), outline=s_col, width=1)
        draw.text((56, py + 8), step_title, fill=s_col, font=F_BOLD)
        draw.text((56, py + 30), s_line1, fill=C_WHEAT, font=F_BODY)
        draw.text((56, py + 52), s_line2, fill=(140, 170, 180), font=F_MONO_SM)
        
        # Indicator badge
        draw_pill(draw, 425, py + 8, "VERIFIED", C_BLACK, s_col, F_MONO_XS, dot_color=s_col, border_color=s_col)
        
        if step_title != pipe_steps[-1][0]:
            draw.line([(283, py + 80), (283, py + 92)], fill=s_col, width=2)
            draw.polygon([(279, py + 88), (287, py + 88), (283, py + 94)], fill=s_col)
        py += 92

    # Panel 2: MySQL 8.0 Normalized Schema (Center, w=440)
    p2_box = [554, 76, 994, 680]
    draw.rounded_rectangle(p2_box, radius=12, fill=(8, 28, 38), outline=C_SLATE, width=2)
    # Header tab
    draw.rounded_rectangle([554, 76, 994, 114], radius=12, fill=(14, 44, 52), outline=C_SLATE, width=1)
    draw.text((570, 86), "MYSQL 8.0 NORMALIZED RELATIONAL SCHEMA", fill=C_WHEAT, font=F_HEAD)
    draw.text((885, 89), "InnoDB ACID", fill=C_CYAN, font=F_MONO_SM)
    
    # Tables in schema
    tables = [
        ("Table: users (Core Credentials & Identity)", [
            "id: BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY",
            "username: VARCHAR(50) NOT NULL UNIQUE INDEX",
            "email: VARCHAR(100) NOT NULL UNIQUE INDEX",
            "password_hash: CHAR(60) NOT NULL (BCrypt Salted)",
            "is_active: BOOLEAN DEFAULT TRUE",
            "created_at: TIMESTAMP DEFAULT CURRENT_TIMESTAMP"
        ]),
        ("Table: roles & permissions (RBAC Mapping)", [
            "id: INT PRIMARY KEY | name: VARCHAR(30) UNIQUE",
            "roles: ROLE_ADMIN, ROLE_SRE, ROLE_OPERATOR, ROLE_USER",
            "Table: user_roles (user_id FK, role_id FK) Composite PK",
            "Table: role_permissions (role_id FK, permission_id FK)"
        ]),
        ("Table: audit_logs (Immutable Compliance Trail)", [
            "id: BIGINT PK | actor_id: BIGINT | event: VARCHAR(60)",
            "action: [LOGIN_SUCCESS, ROLE_GRANT, PASSWORD_RESET]",
            "ip_address: VARCHAR(45) | user_agent: VARCHAR(255)",
            "timestamp: TIMESTAMP (Partitioned by Month)"
        ])
    ]
    
    ty = 126
    for t_header, t_fields in tables:
        t_box = [570, ty, 978, ty + 24 + len(t_fields)*22]
        draw.rounded_rectangle(t_box, radius=6, fill=(10, 30, 40), outline=C_SLATE, width=1)
        draw.text((582, ty + 8), t_header, fill=C_ORANGE, font=F_BOLD)
        fy = ty + 30
        for f in t_fields:
            draw.text((582, fy), f"- {f}", fill=C_WHEAT if "PRIMARY KEY" in f or "UNIQUE" in f else (150, 180, 190), font=F_MONO_SM)
            fy += 22
        ty += 36 + len(t_fields)*22

    # Panel 3: Redis Blacklist, Token Bucket & Stack (Right, w=354)
    p3_box = [1010, 76, W - 28, 680]
    draw.rounded_rectangle(p3_box, radius=12, fill=(8, 28, 38), outline=C_SLATE, width=2)
    # Header tab
    draw.rounded_rectangle([1010, 76, W - 28, 114], radius=12, fill=(14, 44, 52), outline=C_SLATE, width=1)
    draw.text((1026, 86), "SECURITY CONTROLS & CACHE", fill=C_WHEAT, font=F_HEAD)
    
    # Redis Blacklist
    rb_box = [1026, 126, W - 44, 276]
    draw.rounded_rectangle(rb_box, radius=8, fill=(10, 32, 42), outline=C_RED, width=1)
    draw.text((1038, 138), "Redis Token Blacklist Engine", fill=C_WHEAT, font=F_BOLD)
    draw.text((1038, 164), "- Instant O(1) Token Invalidation on Logout", fill=(160, 190, 200), font=F_MONO_SM)
    draw.text((1038, 188), "- Key: jti:blacklist:<jwt-id>", fill=C_RED, font=F_MONO_SM)
    draw.text((1038, 212), "- Automatic TTL expiry matching token lifetime", fill=(160, 190, 200), font=F_MONO_SM)
    draw.text((1038, 236), "- Zero database hit for blacklisted tokens", fill=C_GREEN, font=F_MONO_SM)
    
    # Rate Limiter
    rl_box = [1026, 290, W - 44, 440]
    draw.rounded_rectangle(rl_box, radius=8, fill=(10, 32, 42), outline=C_CYAN, width=1)
    draw.text((1038, 302), "Brute-Force Rate Limiter", fill=C_WHEAT, font=F_BOLD)
    draw.text((1038, 328), "- Token Bucket Algorithm (Redis backend)", fill=(160, 190, 200), font=F_MONO_SM)
    draw.text((1038, 352), "- Limit: 10 failed auth attempts / 15 mins", fill=C_CYAN, font=F_MONO_SM)
    draw.text((1038, 376), "- Auto IP Jail & CAPTCHA Escalation", fill=(160, 190, 200), font=F_MONO_SM)
    draw.text((1038, 400), "- Status: SHIELD ACTIVE (0 breaches)", fill=C_GREEN, font=F_MONO_SM)
    
    # Verified Tech Stack
    stk_box = [1026, 454, W - 44, 664]
    draw.rounded_rectangle(stk_box, radius=8, fill=(10, 30, 40), outline=C_SLATE, width=1)
    draw.text((1038, 466), "ENTERPRISE TECH STACK", fill=C_WHEAT, font=F_BOLD)
    
    stack = [
        ("Spring Boot 3.2", C_GREEN),
        ("Spring Security 6", C_CYAN),
        ("JWT (RSA-256)", C_WHEAT),
        ("BCrypt (12-salt)", C_ORANGE),
        ("MySQL 8.0", C_CYAN),
        ("Redis 7.2", C_RED),
        ("Docker Container", C_CYAN),
        ("OpenAPI 3 / Swagger", C_GREEN)
    ]
    bx, by = 1038, 498
    for st_name, st_col in stack:
        bw = draw_pill(draw, bx, by, st_name, C_BLACK, st_col, F_MONO_SM, dot_color=st_col, border_color=C_SLATE)
        bx += bw + 8
        if bx > W - 140:
            bx = 1038
            by += 32

    # ---------------- BOTTOM TERMINAL HUD (y=694 to 754) ----------------
    draw.rounded_rectangle([28, 694, W - 28, 754], radius=8, fill=(6, 20, 28), outline=C_SLATE, width=1)
    draw.text((44, 706), "AUTH AUDIT: [200 OK] User 'nikhil.admin' authenticated | JWT issued (TTL: 3600s) | RBAC: [ROLE_ADMIN, ROLE_SRE]", fill=C_GREEN, font=F_MONO)
    draw.text((44, 728), "SECURITY TELEMETRY: 0 active blacklisted sessions | BCrypt hash latency: 84ms | Redis token cache hit rate: 99.4%", fill=(160, 180, 190), font=F_MONO_SM)

    im.save(out_path, quality=95)
    print(f"Successfully generated {out_path}")

# =============================================================
# MAIN ENTRYPOINT
# =============================================================
if __name__ == "__main__":
    wp = r"C:\Users\levak\.gemini\antigravity\scratch\nikhil-portfolio"
    generate_kubeheal_card(os.path.join(wp, "kubeheal_card.jpg"))
    generate_flight_card(os.path.join(wp, "flight_card.jpg"))
    generate_user_card(os.path.join(wp, "user_card.jpg"))
    print("ALL THREE 70% HUMAN / 30% AI PROJECT CARDS GENERATED SUCCESSFULLY!")
