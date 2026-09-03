# main.py
import os
from crewai import Agent, Task, Crew, LLM
from crewai_files import ImageFile  # 处理图片输入

# ============================================
# 1. 配置 DeepSeek 视觉模型
# ============================================
llm = LLM(
    model="deepseek/deepseek-v4-flash-vision-exp", api_key=os.getenv("OPENAI_API_KEY"), base_url="https://api.deepseek.com/v1"  # 换成支持图片的模型
)

# ============================================
# 2. 定义三个 Agent
# ============================================
math_agent = Agent(
    role="高等数学辅导老师",
    goal="帮助理解高等数学的核心概念，解答极限、导数、积分、泰勒展开等题目",
    backstory="你是一位精通高等数学的助教，擅长把抽象公式用通俗语言讲清楚",
    allow_delegation=False,
    llm=llm,
)

physics_agent = Agent(
    role="大学物理辅导老师",
    goal="帮助理解大学物理的基本原理，解答力学、电磁学、热学等题目",
    backstory="你是一位物理系博士生，擅长用生活例子解释物理现象",
    allow_delegation=False,
    llm=llm,
)

planner_agent = Agent(
    role="学习规划师",
    goal="根据学生的学习情况，制定个性化的复习计划",
    backstory="你是一位教育心理学专家，擅长分析学习需求并给出高效建议",
    allow_delegation=True,
    llm=llm,
)


# ============================================
# 3. 核心函数：统一处理文字或图片输入
# ============================================
def run_task(agent, description, image_path=None):
    """让 Agent 执行任务，支持文字和图片两种输入方式"""

    # 如果提供了图片路径，加载图片
    input_files = {}
    if image_path and os.path.exists(image_path):
        print(f"🖼️ 正在读取图片：{image_path}")
        input_files = {"problem_image": ImageFile(source=image_path)}
        # 告诉 Agent 有图片要分析
        description += " 请优先分析图片中的题目内容。"

    # 创建任务
    task = Task(description=description, agent=agent, input_files=input_files)  # 传入图片（如果有）

    crew = Crew(agents=[agent], tasks=[task])
    result = crew.kickoff()

    print("\n" + "=" * 50)
    print("📝 回答：")
    print("=" * 50)
    print(result)
    print("=" * 50)


def get_input_choice():
    """让用户选择输入方式：文字还是图片"""
    print("\n请选择输入方式：")
    print("1. 文字输入（直接打字）")
    print("2. 图片输入（提供图片路径）")
    choice = input("请输入数字选择：").strip()
    return choice


def get_text_input(prompt):
    """获取文字输入"""
    print(prompt)
    return input().strip()


def get_image_input(prompt):
    """获取图片路径"""
    print(prompt)
    print("💡 提示：把图片放在项目文件夹里，直接输入文件名（如：math.jpg）")
    print("   或者输入完整路径（如：D:/images/physics.png）")
    path = input().strip()
    return path if path else None


# ============================================
# 4. 菜单功能
# ============================================
def run_math():
    print("\n📐 高数辅导老师")
    choice = get_input_choice()

    if choice == "1":
        question = get_text_input("请输入你的高数题（文字描述）：")
        if question:
            run_task(math_agent, f"请解答以下高等数学问题：{question}")
        else:
            print("⚠️ 未输入内容，返回主菜单。")
    elif choice == "2":
        img_path = get_image_input("请输入题目的图片路径：")
        if img_path:
            run_task(math_agent, "请分析图片中的高等数学题目并给出解答。", image_path=img_path)
        else:
            print("⚠️ 未提供图片，返回主菜单。")
    else:
        print("❌ 无效选择")


def run_physics():
    print("\n⚛️ 物理辅导老师")
    choice = get_input_choice()

    if choice == "1":
        question = get_text_input("请输入你的物理题（文字描述）：")
        if question:
            run_task(physics_agent, f"请解答以下大学物理问题：{question}")
        else:
            print("⚠️ 未输入内容，返回主菜单。")
    elif choice == "2":
        img_path = get_image_input("请输入题目的图片路径：")
        if img_path:
            run_task(physics_agent, "请分析图片中的大学物理题目并给出解答。", image_path=img_path)
        else:
            print("⚠️ 未提供图片，返回主菜单。")
    else:
        print("❌ 无效选择")


def run_planner():
    print("\n📚 学习规划师")
    choice = get_input_choice()

    if choice == "1":
        desc = get_text_input("请描述你的学习情况（学了什么？哪里卡住了？）：")
        if desc:
            run_task(planner_agent, f"根据以下情况制定复习计划：{desc}")
        else:
            print("⚠️ 未输入内容，返回主菜单。")
    elif choice == "2":
        img_path = get_image_input("请输入包含学习记录的图片路径（如课程表、错题本截图）：")
        if img_path:
            run_task(planner_agent, "请根据图片中的学习记录制定复习计划。", image_path=img_path)
        else:
            print("⚠️ 未提供图片，返回主菜单。")
    else:
        print("❌ 无效选择")


# ============================================
# 5. 主菜单
# ============================================
def show_menu():
    print("\n" + "=" * 40)
    print("🤖 智能学习助手 v2.0（支持图片输入）")
    print("=" * 40)
    print("1. 问高数题（高数辅导老师）")
    print("2. 问物理题（物理辅导老师）")
    print("3. 制定复习计划（学习规划师）")
    print("0. 退出")
    print("=" * 40)


def main():
    print("\n🎓 欢迎使用智能学习助手 v2.0")
    print("📖 支持文字 + 图片输入")

    while True:
        show_menu()
        choice = input("请输入数字选择：").strip()

        if choice == "0":
            print("👋 再见！祝你学习进步！")
            break
        elif choice == "1":
            run_math()
        elif choice == "2":
            run_physics()
        elif choice == "3":
            run_planner()
        else:
            print("❌ 无效选择，请输入 0-3 之间的数字。")


if __name__ == "__main__":
    main()
