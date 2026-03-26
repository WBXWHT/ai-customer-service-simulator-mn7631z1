#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI产品经理实习生项目：智能客服知识库模拟系统
模拟基于大模型的智能客服问答流程，展示意图识别和知识库查询功能
"""

import json
import random
import datetime
from typing import Dict, List, Tuple

class KnowledgeBase:
    """模拟结构化知识库管理类"""
    
    def __init__(self):
        # 模拟结构化知识库数据
        self.knowledge_base = {
            "产品功能": {
                "意图": ["功能咨询", "使用教程", "特性了解"],
                "答案": [
                    "我们的产品支持智能问答、数据分析、自动化报告等功能。",
                    "您可以查看帮助文档或联系技术支持获取详细教程。",
                    "主要特性包括：实时响应、多语言支持、自定义配置。"
                ]
            },
            "账户问题": {
                "意图": ["登录问题", "密码重置", "账户异常"],
                "答案": [
                    "请检查用户名密码是否正确，或尝试找回密码功能。",
                    "您可以通过官网的密码重置页面或联系客服重置密码。",
                    "账户异常请提供账号信息，我们将尽快为您处理。"
                ]
            },
            "技术支持": {
                "意图": ["故障报修", "技术咨询", "系统错误"],
                "答案": [
                    "请描述具体故障现象，我们的工程师会尽快处理。",
                    "技术问题可联系技术支持热线：400-123-4567。",
                    "系统错误请提供错误代码和截图，以便快速定位问题。"
                ]
            }
        }
        
        # 记录历史对话用于优化分析
        self.conversation_history = []
    
    def query_knowledge(self, intent: str) -> str:
        """根据识别出的意图查询知识库"""
        for category, data in self.knowledge_base.items():
            if intent in data["意图"]:
                # 模拟从多个答案中选择最合适的
                return random.choice(data["答案"])
        return "抱歉，我暂时无法回答这个问题，已为您转接人工客服。"

class IntentRecognizer:
    """模拟大模型意图识别器"""
    
    def __init__(self):
        # 模拟经过优化的意图识别模型
        self.intent_patterns = {
            "功能咨询": ["怎么用", "有什么功能", "能做什么", "如何使用"],
            "使用教程": ["教程", "教学", "怎么操作", "步骤"],
            "登录问题": ["登录不了", "无法登录", "登不上去", "登录失败"],
            "密码重置": ["忘记密码", "重置密码", "修改密码", "密码找回"],
            "故障报修": ["坏了", "故障", "不能用", "报修", "维修"],
            "技术咨询": ["技术问题", "咨询技术", "技术支持", "专业问题"]
        }
    
    def recognize_intent(self, user_input: str) -> str:
        """模拟大模型意图识别功能"""
        user_input = user_input.lower()
        
        # 模拟大模型语义理解：匹配关键词和模式
        for intent, patterns in self.intent_patterns.items():
            for pattern in patterns:
                if pattern in user_input:
                    return intent
        
        # 如果无法识别，返回默认意图
        return "未知意图"

class CustomerServiceSimulator:
    """智能客服模拟系统主类"""
    
    def __init__(self):
        self.kb = KnowledgeBase()
        self.recognizer = IntentRecognizer()
        self.stats = {
            "total_queries": 0,
            "resolved_first_round": 0,
            "transferred_to_human": 0,
            "start_time": datetime.datetime.now()
        }
    
    def process_query(self, user_input: str) -> Tuple[str, Dict]:
        """处理用户查询，返回回答和元数据"""
        self.stats["total_queries"] += 1
        
        # 记录对话历史
        conversation_entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "user_input": user_input,
            "session_id": f"session_{self.stats['total_queries']}"
        }
        
        # 步骤1：意图识别
        intent = self.recognizer.recognize_intent(user_input)
        conversation_entry["recognized_intent"] = intent
        
        # 步骤2：知识库查询
        if intent != "未知意图":
            answer = self.kb.query_knowledge(intent)
            self.stats["resolved_first_round"] += 1
            conversation_entry["resolved"] = True
            conversation_entry["answer_source"] = "知识库"
        else:
            answer = "抱歉，我暂时无法理解您的问题，已为您转接人工客服。"
            self.stats["transferred_to_human"] += 1
            conversation_entry["resolved"] = False
            conversation_entry["answer_source"] = "人工转接"
        
        conversation_entry["answer"] = answer
        self.kb.conversation_history.append(conversation_entry)
        
        # 准备返回数据
        metadata = {
            "intent": intent,
            "resolved": intent != "未知意图",
            "timestamp": conversation_entry["timestamp"],
            "session_id": conversation_entry["session_id"]
        }
        
        return answer, metadata
    
    def get_statistics(self) -> Dict:
        """获取系统运行统计信息"""
        if self.stats["total_queries"] == 0:
            return {"error": "暂无查询记录"}
        
        first_round_rate = (self.stats["resolved_first_round"] / self.stats["total_queries"]) * 100
        transfer_rate = (self.stats["transferred_to_human"] / self.stats["total_queries"]) * 100
        
        return {
            "总查询数": self.stats["total_queries"],
            "首轮解决数": self.stats["resolved_first_round"],
            "首轮解决率": f"{first_round_rate:.1f}%",
            "人工转接数": self.stats["transferred_to_human"],
            "人工转接率": f"{transfer_rate:.1f}%",
            "运行时长": str(datetime.datetime.now() - self.stats["start_time"])
        }

def main():
    """主函数：智能客服系统演示"""
    print("=" * 60)
    print("智能客服知识库优化模拟系统")
    print("纪元AI - AI产品经理实习生项目")
    print("=" * 60)
    
    # 初始化客服系统
    css = CustomerServiceSimulator()
    
    # 模拟用户查询示例
    example_queries = [
        "这个产品有什么功能？",
        "我忘记密码了怎么办？",
        "登录不了系统",
        "怎么使用数据分析功能？",
        "设备坏了需要维修",
        "今天天气怎么样？"  # 测试未知意图
    ]
    
    print("\n模拟用户对话流程：")
    print("-" * 40)
    
    # 处理示例查询
    for i, query in enumerate(example_queries, 1):
        print(f"\n用户{i}: {query}")
        answer, metadata = css.process_query(query)
        print(f"客服: {answer}")
        print(f"   [意图识别: {metadata['intent']}, 是否解决: {metadata['resolved']}]")
    
    # 显示统计信息
    print("\n" + "=" * 60)
    print("系统运行统计：")
    print("-" * 40)
    
    stats = css.get_statistics()
    for key, value in stats.items():
        print(f"{key}: {value}")
    
    # 模拟项目成果展示
    print("\n" + "=" * 60)
    print("项目成果模拟（基于历史数据优化）：")
    print("-" * 40)
    print("• 意图识别准确率提升: 15%")
    print("• 首轮问题解决率提升: 18%")
    print("• 人工客服转接率降低: 25%")
    print("• 知识库结构化覆盖率: 85%")
    print("=" * 60)
    
    # 保存对话历史（模拟）
    print(f"\n对话历史已记录，共 {len(css.kb.conversation_history)} 条记录")
    print("系统运行完成！")

if __name__ == "__main__":
    main()