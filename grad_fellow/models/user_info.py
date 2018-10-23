# -*- coding:utf-8 -*-
"""Model: UserInfo."""
from ..db import db


class UserInfo(db.Model):
    """UserInfo."""

    # 自增id
    id = db.Column(db.Integer, primary_key=True)
    # 用户名（外键 user.name）
    name = db.Column(db.String(100), db.ForeignKey('user.name'),
                     unique=True, nullable=False)

    # -------------------------- Basic Info ----------------------
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    # 当前职位
    position = db.Column(db.String(100), nullable=False)
    # 当前就职公司
    company = db.Column(db.String(100))
    # 国籍
    nationality = db.Column(db.String(100), nullable=False)
    # 是否愿意被联系
    tobe_contacted = db.Column(db.Boolean)

    # -------------------------- Skills --------------------------
    # 拥有的技能
    skills_have = db.Column(db.Text)
    # 学习到的技能
    skills_learned = db.Column(db.Text)
    # 推荐的技能
    skills_recommend = db.Column(db.Text)
    # 工作中需要沟通的角色
    skills_roles_in_company = db.Column(db.Text)
    # 自主完成的任务
    skills_tasks_auto = db.Column(db.Text)
    # 协作完成的任务
    skills_tasks_collab = db.Column(db.Text)

    # -------------------------- Company Culture -----------------
    cc_competitiveness = db.Column(db.Text)
    cc_desc_by_colleagues = db.Column(db.Text)
    cc_working_approach = db.Column(db.Text)
    cc_relationship_with_colleague = db.Column(db.Text)
    cc_relationship_with_mgr = db.Column(db.Text)

    def __repr__(self):
        """Provide usable string representations of itself."""
        return '<UserInfo name=%r>' % self.name
