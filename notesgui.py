#!/usr/bin/env python3
# DEVELOPER: root0emir 
import sys
import os
import json
import csv
from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                           QHBoxLayout, QLabel, QLineEdit, QTextEdit, 
                           QPushButton, QComboBox, QListWidget, QListWidgetItem,
                           QMessageBox, QFileDialog, QCalendarWidget, QDialog,
                           QTabWidget, QFrame, QScrollArea, QCheckBox,
                           QSpinBox, QColorDialog, QFontDialog, QMenuBar,
                           QMenu, QAction, QStatusBar, QToolBar, QToolButton,
                           QInputDialog, QSplitter, QStyle, QStyleFactory,
                           QStyleOptionButton)
from PyQt5.QtCore import Qt, QSize, QTimer, QDateTime, QPropertyAnimation, QEasingCurve, pyqtSignal, QDate
from PyQt5.QtGui import QFont, QIcon, QColor, QPalette, QTextCharFormat, QLinearGradient, QPainter
from cryptography.fernet import Fernet

# Securonis Notes GUI Developed by root0emir Version 2.5

class ModernCheckBox(QCheckBox):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setStyleSheet("""
            QCheckBox {
                color: white;
                font-weight: bold;
                padding: 5px;
                border-radius: 4px;
            }
            QCheckBox::indicator {
                width: 24px;
                height: 24px;
            }
            QCheckBox::indicator:unchecked {
                border: 2px solid #4d4d4d;
                background-color: #2d2d2d;
                border-radius: 4px;
            }
            QCheckBox::indicator:checked {
                border: 2px solid #4d4d4d;
                background-color: #4d4d4d;
                border-radius: 4px;
            }
            QCheckBox::indicator:checked:hover {
                border: 2px solid #5d5d5d;
                background-color: #5d5d5d;
            }
            QCheckBox::indicator:unchecked:hover {
                border: 2px solid #5d5d5d;
                background-color: #3d3d3d;
            }
            QCheckBox::indicator:pressed {
                border: 2px solid #3d3d3d;
                background-color: #2d2d2d;
            }
        """)
        self.setCursor(Qt.PointingHandCursor)
        
    def paintEvent(self, event):
        super().paintEvent(event)
        if self.isChecked():
            painter = QPainter(self)
            painter.setPen(Qt.white)
            painter.setFont(QFont("Arial", 16))
            

            style = self.style()
            opt = QStyleOptionButton()
            self.initStyleOption(opt)
            indicator_rect = style.subElementRect(QStyle.SE_CheckBoxIndicator, opt, self)
            
           
            painter.drawText(indicator_rect, Qt.AlignCenter | Qt.AlignVCenter, "✓")

class ModernButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setStyleSheet("""
            QPushButton {
                background-color: #2d2d2d;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #3d3d3d;
            }
            QPushButton:pressed {
                background-color: #1d1d1d;
            }
        """)
        self.setCursor(Qt.PointingHandCursor)
        
        # Add hover animation
        self.animation = QPropertyAnimation(self, b"geometry")
        self.animation.setDuration(100)
        self.animation.setEasingCurve(QEasingCurve.OutCubic)
        
    def enterEvent(self, event):
        self.animation.setStartValue(self.geometry())
        self.animation.setEndValue(self.geometry().adjusted(-2, -2, 2, 2))
        self.animation.start()
        
    def leaveEvent(self, event):
        self.animation.setStartValue(self.geometry())
        self.animation.setEndValue(self.geometry().adjusted(2, 2, -2, -2))
        self.animation.start()

class CategoryManager(QDialog):
    def __init__(self, parent=None, categories=None):
        super().__init__(parent)
        self.categories = categories or []
        self.setup_ui()
        
    def setup_ui(self):
        self.setWindowTitle("Category Manager")
        self.setGeometry(300, 300, 400, 500)
        self.setStyleSheet("""
            QDialog {
                background-color: #1d1d1d;
                color: white;
            }
        """)
        
        layout = QVBoxLayout()

        category_label = QLabel("Current Categories:")
        category_label.setStyleSheet("color: #ffffff; font-weight: bold; font-size: 14px;")
        layout.addWidget(category_label)
        
        self.category_list = QListWidget()
        self.category_list.setStyleSheet("""
            QListWidget {
                background-color: #2d2d2d;
                color: white;
                border: 1px solid #3d3d3d;
                border-radius: 4px;
                padding: 5px;
            }
            QListWidget::item {
                padding: 8px;
                border-radius: 4px;
            }
            QListWidget::item:selected {
                background-color: #4d4d4d;
                color: white;
            }
            QListWidget::item:hover {
                background-color: #3d3d3d;
            }
        """)
        layout.addWidget(self.category_list)
        
        add_layout = QHBoxLayout()
        self.new_category = QLineEdit()
        self.new_category.setPlaceholderText("Add new category...")
        self.new_category.setStyleSheet("""
            QLineEdit {
                background-color: #2d2d2d;
                color: white;
                border: 1px solid #3d3d3d;
                padding: 8px;
                border-radius: 4px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 1px solid #4d4d4d;
            }
        """)
        
        add_button = ModernButton("Add")
        add_button.clicked.connect(self.add_category)
        add_layout.addWidget(self.new_category)
        add_layout.addWidget(add_button)
        layout.addLayout(add_layout)
        
    
        delete_button = ModernButton("Delete Selected")
        delete_button.clicked.connect(self.delete_category)
        layout.addWidget(delete_button)
        
       
        close_button = ModernButton("Close")
        close_button.clicked.connect(self.accept)
        layout.addWidget(close_button)
        
        self.setLayout(layout)
        
  
        self.update_category_list()
        
    def update_category_list(self):
        self.category_list.clear()
        for category in sorted(self.categories):
            self.category_list.addItem(category)
            
    def add_category(self):
        category = self.new_category.text().strip()
        if category and category not in self.categories:
            self.categories.append(category)
            self.update_category_list()
            self.new_category.clear()
            
    def delete_category(self):
        selected_items = self.category_list.selectedItems()
        if selected_items:
            category = selected_items[0].text()
            if category in self.categories:
                self.categories.remove(category)
                self.update_category_list()
                
    def get_categories(self):
        return self.categories

class TagManager(QDialog):
    def __init__(self, parent=None, tags=None):
        super().__init__(parent)
        self.tags = tags or []
        self.setup_ui()
        
    def setup_ui(self):
        self.setWindowTitle("Tag Manager")
        self.setGeometry(300, 300, 400, 500)
        self.setStyleSheet("""
            QDialog {
                background-color: #1d1d1d;
                color: white;
            }
        """)
        
        layout = QVBoxLayout()
        
 
        tag_label = QLabel("Current Tags:")
        tag_label.setStyleSheet("color: #ffffff; font-weight: bold; font-size: 14px;")
        layout.addWidget(tag_label)
        
        self.tag_list = QListWidget()
        self.tag_list.setStyleSheet("""
            QListWidget {
                background-color: #2d2d2d;
                color: white;
                border: 1px solid #3d3d3d;
                border-radius: 4px;
                padding: 5px;
            }
            QListWidget::item {
                padding: 8px;
                border-radius: 4px;
            }
            QListWidget::item:selected {
                background-color: #4d4d4d;
                color: white;
            }
            QListWidget::item:hover {
                background-color: #3d3d3d;
            }
        """)
        layout.addWidget(self.tag_list)
        

        add_layout = QHBoxLayout()
        self.new_tag = QLineEdit()
        self.new_tag.setPlaceholderText("Add new tag...")
        self.new_tag.setStyleSheet("""
            QLineEdit {
                background-color: #2d2d2d;
                color: white;8
                border: 1px solid #3d3d3d;
                padding: 8px;
                border-radius: 4px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 1px solid #4d4d4d;
            }
        """)
        
        add_button = ModernButton("Add")
        add_button.clicked.connect(self.add_tag)
        add_layout.addWidget(self.new_tag)
        add_layout.addWidget(add_button)
        layout.addLayout(add_layout)
        

        delete_button = ModernButton("Delete Selected")
        delete_button.clicked.connect(self.delete_tag)
        layout.addWidget(delete_button)
        

        close_button = ModernButton("Close")
        close_button.clicked.connect(self.accept)
        layout.addWidget(close_button)
        
        self.setLayout(layout)
        
  
        self.update_tag_list()
        
    def update_tag_list(self):
        self.tag_list.clear()
        for tag in sorted(self.tags):
            self.tag_list.addItem(tag)
            
    def add_tag(self):
        tag = self.new_tag.text().strip()
        if tag and tag not in self.tags:
            self.tags.append(tag)
            self.update_tag_list()
            self.new_tag.clear()
            
    def delete_tag(self):
        selected_items = self.tag_list.selectedItems()
        if selected_items:
            tag = selected_items[0].text()
            if tag in self.tags:
                self.tags.remove(tag)
                self.update_tag_list()
                
    def get_tags(self):
        return self.tags

class Note:
    def __init__(self, title="", content="", tags=None, priority="low",
                 due_date=None, category="general", color="#ffffff",
                 font_family="Arial", font_size=10, is_encrypted=False):
        self.title = title
        self.content = content
        self.tags = tags or []
        self.priority = priority
        self.due_date = due_date or datetime.now()
        self.category = category
        self.color = color
        self.font_family = font_family
        self.font_size = font_size
        self.is_encrypted = is_encrypted
        self.created_at = datetime.now()
        self.modified_at = datetime.now()
        self.attachments = []  
        self.reminder = None
        self.is_favorite = False
        self.is_archived = False
        
    def __eq__(self, other):
    
        if not isinstance(other, Note):
            return False
        return (self.title == other.title and 
                self.content == other.content and
                self.created_at == other.created_at)
        
    def add_attachment(self, file_path):
      
        file_name = os.path.basename(file_path)
        
        file_size = os.path.getsize(file_path)
        if file_size > 10 * 1024 * 1024:  
            raise ValueError("File size exceeds the 10MB limit.")
            
   
        allowed_extensions = ['.txt', '.pdf', '.doc', '.docx', '.jpg', '.jpeg', '.png', '.gif']
        file_extension = os.path.splitext(file_name)[1].lower()
        if file_extension not in allowed_extensions:
            raise ValueError(f"File type {file_extension} is not allowed.")
            
        try:
            with open(file_path, 'rb') as file:
                file_content = file.read()
      
                import base64
                encoded_content = base64.b64encode(file_content).decode('utf-8')
                
                if len(self.attachments) >= 10:
                    raise ValueError("Maximum 10 attachments allowed per note.")
                    
                self.attachments.append({
                    'name': file_name,
                    'content': encoded_content,
                    'size': file_size,
                    'type': file_extension,
                    'added_time': datetime.now().isoformat()
                })
                return True
        except Exception as e:
            print(f"Dosya ekleme hatası: {str(e)}")
            raise e
            
    def get_attachment(self, file_name):
    
        for attachment in self.attachments:
            if attachment['name'] == file_name:
                import base64
                return base64.b64decode(attachment['content'])
        return None

    def to_dict(self):
      
        return {
            'title': self.title,
            'content': self.content,
            'tags': self.tags,
            'priority': self.priority,
            'due_date': self.due_date.isoformat(),
            'category': self.category,
            'color': self.color,
            'font_family': self.font_family,
            'font_size': self.font_size,
            'is_encrypted': self.is_encrypted,
            'created_at': self.created_at.isoformat(),
            'modified_at': self.modified_at.isoformat(),
            'attachments': self.attachments,
            'reminder': self.reminder.isoformat() if self.reminder else None,
            'is_favorite': self.is_favorite,
            'is_archived': self.is_archived
        }
        
    @classmethod
    def from_dict(cls, data):

        note = cls()
        note.title = data.get('title', '')
        note.content = data.get('content', '')
        note.tags = data.get('tags', [])
        note.priority = data.get('priority', 'low')
        
    
        try:
            note.due_date = datetime.fromisoformat(data.get('due_date', datetime.now().isoformat()))
        except (ValueError, TypeError):
            note.due_date = datetime.now()
            
        try:
            note.created_at = datetime.fromisoformat(data.get('created_at', datetime.now().isoformat()))
        except (ValueError, TypeError):
            note.created_at = datetime.now()
            
        try:
            note.modified_at = datetime.fromisoformat(data.get('modified_at', datetime.now().isoformat()))
        except (ValueError, TypeError):
            note.modified_at = datetime.now()
            
        note.category = data.get('category', 'general')
        note.color = data.get('color', '#ffffff')
        note.font_family = data.get('font_family', 'Arial')
        note.font_size = data.get('font_size', 10)
        note.is_encrypted = data.get('is_encrypted', False)
        note.attachments = data.get('attachments', [])
        
 
        reminder_str = data.get('reminder')
        if reminder_str:
            try:
                note.reminder = datetime.fromisoformat(reminder_str)
            except (ValueError, TypeError):
                note.reminder = None
        else:
            note.reminder = None
            
        note.is_favorite = data.get('is_favorite', False)
        note.is_archived = data.get('is_archived', False)
        return note

class NoteEditor(QWidget):
    reminder_changed = pyqtSignal(int)  
    attachment_changed = pyqtSignal(int)  
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(10)
        layout.setContentsMargins(10, 10, 10, 10)
        

        title_label = QLabel("Title:")
        title_label.setStyleSheet("color: #ffffff; font-weight: bold; font-size: 14px;")
        self.title_edit = QLineEdit()
        self.title_edit.setPlaceholderText("Enter note title...")
        self.title_edit.setStyleSheet("""
            QLineEdit {
                background-color: #2d2d2d;
                color: white;
                border: 1px solid #3d3d3d;
                padding: 10px;
                border-radius: 5px;
                font-size: 16px;
                font-weight: bold;
            }
            QLineEdit:focus {
                border: 1px solid #4d9de0;
                background-color: #333333;
            }
        """)
        layout.addWidget(title_label)
        layout.addWidget(self.title_edit)
        

        content_label = QLabel("Content:")
        content_label.setStyleSheet("color: #ffffff; font-weight: bold; font-size: 14px;")
        self.content_edit = QTextEdit()
        self.content_edit.setStyleSheet("""
            QTextEdit {
                background-color: #2d2d2d;
                color: white;
                border: 1px solid #3d3d3d;
                padding: 10px;
                border-radius: 5px;
                font-size: 14px;
                line-height: 1.5;
            }
            QTextEdit:focus {
                border: 1px solid #4d9de0;
                background-color: #333333;
            }
        """)
        layout.addWidget(content_label)
        layout.addWidget(self.content_edit)
        

        bottom_layout = QHBoxLayout()
        

        left_panel = QVBoxLayout()
        
   
        tags_label = QLabel("Tags:")
        tags_label.setStyleSheet("color: #ffffff; font-weight: bold; font-size: 14px;")
        self.tags_edit = QLineEdit()
        self.tags_edit.setPlaceholderText("Enter tags separated by commas...")
        self.tags_edit.setStyleSheet("""
            QLineEdit {
                background-color: #2d2d2d;
                color: white;
                border: 1px solid #3d3d3d;
                padding: 8px;
                border-radius: 5px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 1px solid #4d9de0;
                background-color: #333333;
            }
        """)
        left_panel.addWidget(tags_label)
        left_panel.addWidget(self.tags_edit)
        

        priority_label = QLabel("Priority:")
        priority_label.setStyleSheet("color: #ffffff; font-weight: bold; font-size: 14px;")
        self.priority_combo = QComboBox()
        self.priority_combo.addItems(["low", "medium", "high"])
        self.priority_combo.setStyleSheet("""
            QComboBox {
                background-color: #2d2d2d;
                color: white;
                border: 1px solid #3d3d3d;
                padding: 8px;
                border-radius: 5px;
                font-size: 14px;
                min-width: 150px;
            }
            QComboBox:focus {
                border: 1px solid #4d9de0;
                background-color: #333333;
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 30px;
                border-left: 1px solid #3d3d3d;
            }
            QComboBox QAbstractItemView {
                background-color: #2d2d2d;
                color: white;
                selection-background-color: #4d9de0;
                selection-color: white;
            }
        """)
        left_panel.addWidget(priority_label)
        left_panel.addWidget(self.priority_combo)
        

        category_label = QLabel("Category:")
        category_label.setStyleSheet("color: #ffffff; font-weight: bold; font-size: 14px;")
        self.category_combo = QComboBox()
        self.category_combo.addItems(["general", "work", "personal", "ideas", "tasks"])
        self.category_combo.setStyleSheet("""
            QComboBox {
                background-color: #2d2d2d;
                color: white;
                border: 1px solid #3d3d3d;
                padding: 8px;
                border-radius: 5px;
                font-size: 14px;
                min-width: 150px;
            }
            QComboBox:focus {
                border: 1px solid #4d9de0;
                background-color: #333333;
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 30px;
                border-left: 1px solid #3d3d3d;
            }
            QComboBox QAbstractItemView {
                background-color: #2d2d2d;
                color: white;
                selection-background-color: #4d9de0;
                selection-color: white;
            }
        """)
        left_panel.addWidget(category_label)
        left_panel.addWidget(self.category_combo)
        
    
        right_panel = QVBoxLayout()
        

        due_date_label = QLabel("Due Date:")
        due_date_label.setStyleSheet("color: #ffffff; font-weight: bold; font-size: 14px;")
        self.due_date_edit = QLineEdit()
        self.due_date_edit.setText(datetime.now().strftime("%Y-%m-%d %H:%M"))
        self.due_date_edit.setStyleSheet("""
            QLineEdit {
                background-color: #2d2d2d;
                color: white;
                border: 1px solid #3d3d3d;
                padding: 8px;
                border-radius: 5px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 1px solid #4d9de0;
                background-color: #333333;
            }
        """)
        calendar_button = ModernButton("📅")
        calendar_button.setFixedSize(40, 35)
        calendar_button.clicked.connect(self.show_calendar)
        due_date_layout = QHBoxLayout()
        due_date_layout.addWidget(self.due_date_edit)
        due_date_layout.addWidget(calendar_button)
        right_panel.addWidget(due_date_label)
        right_panel.addLayout(due_date_layout)
        
  
        check_label = QLabel("Options:")
        check_label.setStyleSheet("color: #ffffff; font-weight: bold; font-size: 14px;")
        right_panel.addWidget(check_label)
        

        self.encrypt_check = ModernCheckBox("Encrypt")
        right_panel.addWidget(self.encrypt_check)
        

        self.favorite_check = ModernCheckBox("Favorite")
        right_panel.addWidget(self.favorite_check)
        

        self.archive_check = ModernCheckBox("Archive")
        right_panel.addWidget(self.archive_check)
        

        self.reminder_check = ModernCheckBox("Set Reminder")
        self.reminder_check.stateChanged.connect(self.on_reminder_changed)
        right_panel.addWidget(self.reminder_check)
        

        self.attachment_check = ModernCheckBox("Attachments")
        self.attachment_check.stateChanged.connect(self.on_attachment_changed)
        right_panel.addWidget(self.attachment_check)

        bottom_layout.addLayout(left_panel)
        bottom_layout.addLayout(right_panel)
        layout.addLayout(bottom_layout)
        

        button_layout = QHBoxLayout()
        

        save_button = ModernButton("Save")
        save_button.setStyleSheet("""
            QPushButton {
                background-color: #4d9de0;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #5db9e6;
            }
            QPushButton:pressed {
                background-color: #3d7de0;
            }
        """)
        save_button.clicked.connect(self.save_note)
        button_layout.addWidget(save_button)
        
  
        clear_button = ModernButton("Clear Form")
        clear_button.clicked.connect(self.clear_form)
        button_layout.addWidget(clear_button)
        

        color_button = ModernButton("Text Color")
        color_button.clicked.connect(self.choose_color)
        button_layout.addWidget(color_button)
        
      
        font_button = ModernButton("Text Font")
        font_button.clicked.connect(self.choose_font)
        button_layout.addWidget(font_button)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def choose_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.content_edit.setTextColor(color)
    
    def choose_font(self):
        font, ok = QFontDialog.getFont()
        if ok:
            self.content_edit.setFont(font)

    def clear_form(self):
        self.title_edit.clear()
        self.content_edit.clear()
        self.tags_edit.clear()
        self.priority_combo.setCurrentText("low")
        self.category_combo.setCurrentText("general")
        self.due_date_edit.setText(datetime.now().strftime("%Y-%m-%d %H:%M"))
        self.encrypt_check.setChecked(False)
        self.favorite_check.setChecked(False)
        self.archive_check.setChecked(False)
        self.reminder_check.setChecked(False)
        self.attachment_check.setChecked(False)
        
    def save_note(self):
    
        main_window = self.get_main_window()
        if main_window:
            main_window.save_note()
        else:
        
            note = Note()
            note.title = self.title_edit.text()
            note.content = self.content_edit.toPlainText()
            note.tags = [tag.strip() for tag in self.tags_edit.text().split(",") if tag.strip()]
            note.priority = self.priority_combo.currentText()
            note.category = self.category_combo.currentText()
            note.due_date = datetime.strptime(self.due_date_edit.text(), "%Y-%m-%d %H:%M")
            note.is_encrypted = self.encrypt_check.isChecked()
            note.is_favorite = self.favorite_check.isChecked()
            note.is_archived = self.archive_check.isChecked()
            note.modified_at = datetime.now()
            

            main_window = self.get_main_window()
            if main_window:
                main_window.add_note(note)
                QMessageBox.information(self, "Success", "Note saved successfully!")
            else:
                QMessageBox.warning(self, "Error", "Note could not be saved: Main window not found.")

    def get_main_window(self):

        parent = self.parent()
        while parent is not None and not isinstance(parent, MainWindow):
            parent = parent.parent()
        return parent

    def show_calendar(self):
 
        dialog = QDialog(self)
        dialog.setWindowTitle("Select Date")
        dialog.setGeometry(300, 300, 400, 400)
        dialog.setStyleSheet("""
            QDialog {
                background-color: #2d2d2d;
                color: white;
            }
        """)
        
        layout = QVBoxLayout()
        
        calendar = QCalendarWidget()
        calendar.setStyleSheet("""
            QCalendarWidget {
                background-color: #2d2d2d;
                color: white;
            }
            QCalendarWidget QToolButton {
                color: white;
                background-color: #3d3d3d;
                border: 1px solid #4d4d4d;
                border-radius: 4px;
            }
            QCalendarWidget QMenu {
                background-color: #2d2d2d;
                color: white;
            }
            QCalendarWidget QSpinBox {
                background-color: #2d2d2d;
                color: white;
                border: 1px solid #4d4d4d;
            }
            QCalendarWidget QAbstractItemView:enabled {
                color: white;
                background-color: #3d3d3d;
                selection-background-color: #4d9de0;
                selection-color: white;
            }
            QCalendarWidget QWidget#qt_calendar_navigationbar {
                background-color: #2d2d2d;
            }
        """)
        layout.addWidget(calendar)
        
        time_layout = QHBoxLayout()
        time_label = QLabel("Time (HH:MM):")
        time_label.setStyleSheet("color: white;")
        time_edit = QLineEdit()
        time_edit.setText(datetime.now().strftime("%H:%M"))
        time_edit.setStyleSheet("""
            QLineEdit {
                background-color: #2d2d2d;
                color: white;
                border: 1px solid #3d3d3d;
                padding: 5px;
                border-radius: 4px;
            }
        """)
        time_layout.addWidget(time_label)
        time_layout.addWidget(time_edit)
        layout.addLayout(time_layout)
        
        button_layout = QHBoxLayout()
        ok_button = ModernButton("OK")
        cancel_button = ModernButton("Cancel")
        button_layout.addWidget(ok_button)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)
        
        dialog.setLayout(layout)
        
        def update_date():
            selected_date = calendar.selectedDate().toPyDate()
            time_text = time_edit.text()
            try:
                selected_time = datetime.strptime(time_text, "%H:%M").time()
                full_datetime = datetime.combine(selected_date, selected_time)
                self.due_date_edit.setText(full_datetime.strftime("%Y-%m-%d %H:%M"))
                dialog.accept()
            except ValueError:
                QMessageBox.warning(dialog, "Error", "Invalid time format. Use HH:MM.")
        
        ok_button.clicked.connect(update_date)
        cancel_button.clicked.connect(dialog.reject)
        
        dialog.exec_()

    def on_reminder_changed(self, state):
        self.reminder_changed.emit(state)
    
    def on_attachment_changed(self, state):
        self.attachment_changed.emit(state)

class NoteList(QWidget):
 
    note_selected = pyqtSignal(object)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(10)
        layout.setContentsMargins(10, 10, 10, 10)
        
  
        search_layout = QHBoxLayout()
        search_label = QLabel("Search:")
        search_label.setStyleSheet("color: #ffffff; font-weight: bold; font-size: 14px;")
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("Search notes...")
        self.search_edit.setStyleSheet("""
            QLineEdit {
                background-color: #2d2d2d;
                color: white;
                border: 1px solid #3d3d3d;
                padding: 8px;
                border-radius: 4px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 1px solid #4d4d4d;
            }
        """)
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_edit)
        layout.addLayout(search_layout)
        

        filter_layout = QHBoxLayout()
        
        self.priority_filter = QComboBox()
        self.priority_filter.addItems(["All", "Low", "Medium", "High"])
        self.priority_filter.setStyleSheet("""
            QComboBox {
                background-color: #2d2d2d;
                color: white;
                border: 1px solid #3d3d3d;
                padding: 8px;
                border-radius: 4px;
                font-size: 14px;
            }
            QComboBox:hover {
                border: 1px solid #4d4d4d;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            QComboBox::down-arrow {
                image: url(down_arrow.png);
                width: 12px;
                height: 12px;
            }
        """)
        filter_layout.addWidget(QLabel("Priority:"))
        filter_layout.addWidget(self.priority_filter)
        
        self.category_filter = QComboBox()
        self.category_filter.addItems(["All", "General", "Work", "Personal", "Ideas"])
        self.category_filter.setEditable(True)
        self.category_filter.setStyleSheet("""
            QComboBox {
                background-color: #2d2d2d;
                color: white;
                border: 1px solid #3d3d3d;
                padding: 8px;
                border-radius: 4px;
                font-size: 14px;
            }
            QComboBox:hover {
                border: 1px solid #4d4d4d;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            QComboBox::down-arrow {
                image: url(down_arrow.png);
                width: 12px;
                height: 12px;
            }
        """)
        filter_layout.addWidget(QLabel("Category:"))
        filter_layout.addWidget(self.category_filter)
        
        layout.addLayout(filter_layout)
        
        # View options
        view_layout = QHBoxLayout()
        
        self.show_favorites = ModernCheckBox("Show Favorites")
        view_layout.addWidget(self.show_favorites)
        
        self.show_archived = ModernCheckBox("Show Archived")
        view_layout.addWidget(self.show_archived)
        
        self.show_encrypted = ModernCheckBox("Show Encrypted")
        view_layout.addWidget(self.show_encrypted)
        
        layout.addLayout(view_layout)
        
        # Note List with modern styling
        self.note_list = QListWidget()
        self.note_list.setStyleSheet("""
            QListWidget {
                background-color: #2d2d2d;
                color: white;
                border: 1px solid #3d3d3d;
                border-radius: 4px;
                padding: 5px;
            }
            QListWidget::item {
                padding: 8px;
                border-radius: 4px;
            }
            QListWidget::item:selected {
                background-color: #4d4d4d;
                color: white;
            }
            QListWidget::item:hover {
                background-color: #3d3d3d;
            }
        """)
        layout.addWidget(self.note_list)
        
        self.note_list.itemClicked.connect(self.on_note_clicked)
        
        # Statistics
        stats_layout = QHBoxLayout()
        
        self.total_notes = QLabel("Total Notes: 0")
        self.total_notes.setStyleSheet("color: #ffffff; font-size: 12px;")
        stats_layout.addWidget(self.total_notes)
        
        self.favorite_notes = QLabel("Favorites: 0")
        self.favorite_notes.setStyleSheet("color: #ffffff; font-size: 12px;")
        stats_layout.addWidget(self.favorite_notes)
        
        self.archived_notes = QLabel("Archived: 0")
        self.archived_notes.setStyleSheet("color: #ffffff; font-size: 12px;")
        stats_layout.addWidget(self.archived_notes)
        
        layout.addLayout(stats_layout)
        
        self.setLayout(layout)
        
    def update_statistics(self, notes):
        total = len(notes)
        favorites = sum(1 for note in notes if note.is_favorite)
        archived = sum(1 for note in notes if note.is_archived)
        
        self.total_notes.setText(f"Total Notes: {total}")
        self.favorite_notes.setText(f"Favorites: {favorites}")
        self.archived_notes.setText(f"Archived: {archived}")

    def on_note_clicked(self, item):
        note = item.data(Qt.UserRole)
        self.note_selected.emit(note)

class CalendarView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout()
        
        self.calendar = QCalendarWidget()
        self.calendar.setStyleSheet("""
            QCalendarWidget {
                background-color: #2d2d2d;
                color: white;
                border: 1px solid #3d3d3d;
                border-radius: 4px;
            }
            QCalendarWidget QToolButton {
                color: white;
                background-color: #2d2d2d;
                border: 1px solid #3d3d3d;
                border-radius: 4px;
                padding: 5px;
            }
            QCalendarWidget QMenu {
                background-color: #2d2d2d;
                color: white;
                border: 1px solid #3d3d3d;
            }
            QCalendarWidget QSpinBox {
                background-color: #2d2d2d;
                color: white;
                border: 1px solid #3d3d3d;
                border-radius: 4px;
            }
        """)
        self.calendar.clicked.connect(self.on_date_selected)
        layout.addWidget(self.calendar)
        
        self.note_list = QListWidget()
        self.note_list.setStyleSheet("""
            QListWidget {
                background-color: #2d2d2d;
                color: white;
                border: 1px solid #3d3d3d;
                border-radius: 4px;
                padding: 5px;
            }
            QListWidget::item {
                padding: 8px;
                border-radius: 4px;
            }
            QListWidget::item:selected {
                background-color: #4d4d4d;
                color: white;
            }
            QListWidget::item:hover {
                background-color: #3d3d3d;
            }
        """)
        layout.addWidget(self.note_list)
        
        self.setLayout(layout)
        
    def on_date_selected(self, date):

        self.note_list.clear()
        if hasattr(self.parent(), 'notes'):
            selected_date = date.toPyDate()
            for note in self.parent().notes:
                if note.due_date.date() == selected_date:
                    item = QListWidgetItem(note.title)
                    item.setData(Qt.UserRole, note)
                    self.note_list.addItem(item)
                    
    def update_notes(self, notes):
 
        if hasattr(self, 'calendar'):
         
            self.calendar.setDateTextFormat(QDate(), QTextCharFormat())
            
         
            for note in notes:
                date = note.due_date.date()
                format = QTextCharFormat()
                format.setBackground(QColor(42, 130, 218))
                format.setForeground(QColor(255, 255, 255))
                self.calendar.setDateTextFormat(date, format)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.notes = []
        self.current_note = None
        

        try:
            self.load_encryption_key()
        except Exception as e:
            QMessageBox.warning(self, "Encryption Error", 
                              f"Error loading encryption key: {str(e)}\nEncryption features will be disabled.")
            self.encryption_key = None
        
        try:
            self.setup_ui()
        except Exception as e:
            QMessageBox.critical(self, "Setup Error", 
                               f"Error setting up UI: {str(e)}")
            raise e
        
        try:
            self.load_notes()
        except Exception as e:
            QMessageBox.warning(self, "Load Error", 
                              f"Error loading notes: {str(e)}\nA new empty note file will be created.")
            self.notes = []
            
        # Check reminders periodically
        self.reminder_timer = QTimer(self)
        self.reminder_timer.timeout.connect(self.check_reminders)
        self.reminder_timer.start(60000)  # Check every minute
        
        # Setup status bar
        self.statusBar().showMessage("Ready")
        
    def setup_ui(self):
        # Create central widget and main layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        main_layout = QHBoxLayout()
        main_layout.setSpacing(10)
        
        # Create left panel (note list)
        left_panel = QVBoxLayout()
        
    
        search_layout = QHBoxLayout()
        search_label = QLabel("Search:")
        search_label.setStyleSheet("color: #ffffff; font-weight: bold; font-size: 14px;")
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("Search in notes...")
        self.search_edit.setStyleSheet("""
            QLineEdit {
                background-color: #2d2d2d;
                color: white;
                border: 1px solid #3d3d3d;
                padding: 8px;
                border-radius: 4px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 1px solid #4d4d4d;
            }
        """)
        self.search_edit.textChanged.connect(self.filter_notes)
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_edit)
        left_panel.addLayout(search_layout)
        
 
        tag_filter_layout = QHBoxLayout()
        tag_filter_label = QLabel("Filter by tag:")
        tag_filter_label.setStyleSheet("color: #ffffff; font-weight: bold; font-size: 14px;")
        self.tag_filter_combo = QComboBox()
        self.tag_filter_combo.setStyleSheet("""
            QComboBox {
                background-color: #2d2d2d;
                color: white;
                border: 1px solid #3d3d3d;
                padding: 6px;
                border-radius: 4px;
                font-size: 14px;
            }
            QComboBox:focus {
                border: 1px solid #4d4d4d;
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 20px;
                border-left: 1px solid #3d3d3d;
            }
            QComboBox QAbstractItemView {
                background-color: #2d2d2d;
                color: white;
                selection-background-color: #4d4d4d;
                selection-color: white;
            }
        """)
        self.tag_filter_combo.addItem("All Tags")
        self.tag_filter_combo.currentIndexChanged.connect(self.filter_notes)
        tag_filter_layout.addWidget(tag_filter_label)
        tag_filter_layout.addWidget(self.tag_filter_combo)
        left_panel.addLayout(tag_filter_layout)
        

        self.note_list = NoteList()
        left_panel.addWidget(self.note_list)
        
        # Create right panel (note editor)
        right_panel = QVBoxLayout()
        self.note_editor = NoteEditor()
        right_panel.addWidget(self.note_editor)
        
        # Connect note selection signal
        self.note_list.note_selected.connect(self.on_note_selected)
        
        # Connect editor signals
        self.note_editor.reminder_changed.connect(self.setup_reminder)
        self.note_editor.attachment_changed.connect(self.handle_attachment)
        
        # Add panels to main layout
        main_layout.addLayout(left_panel, 1)
        main_layout.addLayout(right_panel, 2)
        
        self.central_widget.setLayout(main_layout)
        
        # Set window properties
        self.setWindowTitle("Securonis Notes")
        self.setGeometry(100, 100, 1200, 800)
        self.setWindowIcon(QIcon("icon.png"))
        

        self.statusBar().setStyleSheet("background-color: #1d1d1d; color: white;")
        
        # Setup menu and toolbar
        self.setup_menu()
        self.setup_toolbar()
        self.statusBar().showMessage("Ready")
        
    def setup_menu(self):
        menubar = self.menuBar()
        menubar.setStyleSheet("""
            QMenuBar {
                background-color: #1d1d1d;
                color: white;
            }
            QMenuBar::item {
                background-color: #1d1d1d;
                color: white;
                padding: 6px 12px;
            }
            QMenuBar::item:selected {
                background-color: #3d3d3d;
            }
        """)
        
        # File menu
        file_menu = menubar.addMenu("&File")
        file_menu.setStyleSheet("""
            QMenu {
                background-color: #1d1d1d;
                color: white;
                border: 1px solid #3d3d3d;
            }
            QMenu::item {
                padding: 6px 25px 6px 20px;
            }
            QMenu::item:selected {
                background-color: #3d3d3d;
            }
        """)
        
        new_action = QAction(QIcon(self.style().standardIcon(QStyle.SP_FileIcon)), "&New Note", self)
        new_action.setShortcut("Ctrl+N")
        new_action.triggered.connect(self.new_note)
        file_menu.addAction(new_action)
        
        save_action = QAction(QIcon(self.style().standardIcon(QStyle.SP_DialogSaveButton)), "&Save Note", self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.save_note)
        file_menu.addAction(save_action)
        
        delete_action = QAction(QIcon(self.style().standardIcon(QStyle.SP_TrashIcon)), "&Delete Note", self)
        delete_action.setShortcut("Delete")
        delete_action.triggered.connect(self.delete_note)
        file_menu.addAction(delete_action)
        
        file_menu.addSeparator()
        
        backup_action = QAction(QIcon(self.style().standardIcon(QStyle.SP_DialogSaveButton)), "&Backup Notes", self)
        backup_action.triggered.connect(self.backup_notes)
        file_menu.addAction(backup_action)
        
        restore_action = QAction(QIcon(self.style().standardIcon(QStyle.SP_DialogOpenButton)), "&Restore Notes", self)
        restore_action.triggered.connect(self.restore_notes)
        file_menu.addAction(restore_action)
        
        file_menu.addSeparator()
        
        import_action = QAction(QIcon(self.style().standardIcon(QStyle.SP_FileDialogListView)), "&Import Notes", self)
        import_action.triggered.connect(self.import_notes)
        file_menu.addAction(import_action)
        
        export_action = QAction(QIcon(self.style().standardIcon(QStyle.SP_FileDialogDetailedView)), "&Export Notes", self)
        export_action.triggered.connect(self.export_notes)
        file_menu.addAction(export_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction(QIcon(self.style().standardIcon(QStyle.SP_DialogCloseButton)), "&Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Edit menu
        edit_menu = menubar.addMenu("&Edit")
        edit_menu.setStyleSheet("""
            QMenu {
                background-color: #1d1d1d;
                color: white;
                border: 1px solid #3d3d3d;
            }
            QMenu::item {
                padding: 6px 25px 6px 20px;
            }
            QMenu::item:selected {
                background-color: #3d3d3d;
            }
        """)
        
        color_action = QAction(QIcon(self.style().standardIcon(QStyle.SP_DialogResetButton)), "Choose &Color", self)
        color_action.triggered.connect(self.choose_color)
        edit_menu.addAction(color_action)
        
        font_action = QAction(QIcon(self.style().standardIcon(QStyle.SP_DialogResetButton)), "Choose &Font", self)
        font_action.triggered.connect(self.choose_font)
        edit_menu.addAction(font_action)
        
        encrypt_action = QAction(QIcon(self.style().standardIcon(QStyle.SP_DialogResetButton)), "&Encrypt/Decrypt", self)
        encrypt_action.triggered.connect(self.toggle_encryption)
        edit_menu.addAction(encrypt_action)
        
        edit_menu.addSeparator()
        

        manage_menu = menubar.addMenu("&Manage")
        manage_menu.setStyleSheet("""
            QMenu {
                background-color: #1d1d1d;
                color: white;
                border: 1px solid #3d3d3d;
            }
            QMenu::item {
                padding: 6px 25px 6px 20px;
            }
            QMenu::item:selected {
                background-color: #3d3d3d;
            }
        """)
        
        manage_categories_action = QAction("Manage &Categories", self)
        manage_categories_action.triggered.connect(self.manage_categories)
        manage_menu.addAction(manage_categories_action)
        
        manage_tags_action = QAction("Manage &Tags", self)
        manage_tags_action.triggered.connect(self.manage_tags)
        manage_menu.addAction(manage_tags_action)
        
        # View menu
        view_menu = menubar.addMenu("&View")
        view_menu.setStyleSheet("""
            QMenu {
                background-color: #1d1d1d;
                color: white;
                border: 1px solid #3d3d3d;
            }
            QMenu::item {
                padding: 6px 25px 6px 20px;
            }
            QMenu::item:selected {
                background-color: #3d3d3d;
            }
        """)
        
        self.show_favorites_action = QAction("Show Only &Favorites", self)
        self.show_favorites_action.setCheckable(True)
        self.show_favorites_action.triggered.connect(self.toggle_favorites)
        view_menu.addAction(self.show_favorites_action)
        
        self.show_archived_action = QAction("Show Only &Archived", self)
        self.show_archived_action.setCheckable(True)
        self.show_archived_action.triggered.connect(self.toggle_archived)
        view_menu.addAction(self.show_archived_action)
        
        self.show_encrypted_action = QAction("Show Only &Encrypted", self)
        self.show_encrypted_action.setCheckable(True)
        self.show_encrypted_action.triggered.connect(self.filter_notes)
        view_menu.addAction(self.show_encrypted_action)
        
        view_menu.addSeparator()
        
        calendar_action = QAction(QIcon(self.style().standardIcon(QStyle.SP_DialogHelpButton)), "&Calendar View", self)
        calendar_action.triggered.connect(self.show_calendar)
        view_menu.addAction(calendar_action)
        
        # Help menu
        help_menu = menubar.addMenu("&Help")
        help_menu.setStyleSheet("""
            QMenu {
                background-color: #1d1d1d;
                color: white;
                border: 1px solid #3d3d3d;
            }
            QMenu::item {
                padding: 6px 25px 6px 20px;
            }
            QMenu::item:selected {
                background-color: #3d3d3d;
            }
        """)
        
        about_action = QAction(QIcon(self.style().standardIcon(QStyle.SP_DialogHelpButton)), "&About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
        
    def setup_toolbar(self):
        toolbar = QToolBar()
        toolbar.setMovable(False)
        toolbar.setStyleSheet("""
            QToolBar {
                background-color: #2d2d2d;
                border: none;
                spacing: 5px;
                padding: 5px;
            }
        """)
        self.addToolBar(toolbar)
        
        # New note button
        new_btn = QToolButton()
        new_btn.setText("New")
        new_btn.setToolTip("New Note (Ctrl+N)")
        new_btn.clicked.connect(self.new_note)
        toolbar.addWidget(new_btn)
        
        # Save button
        save_btn = QToolButton()
        save_btn.setText("Save")
        save_btn.setToolTip("Save Note (Ctrl+S)")
        save_btn.clicked.connect(self.save_note)
        toolbar.addWidget(save_btn)
        
        toolbar.addSeparator()
        
        # Format buttons
        color_btn = QToolButton()
        color_btn.setText("Color")
        color_btn.setToolTip("Change Text Color")
        color_btn.clicked.connect(self.choose_color)
        toolbar.addWidget(color_btn)
        
        font_btn = QToolButton()
        font_btn.setText("Font")
        font_btn.setToolTip("Change Font")
        font_btn.clicked.connect(self.choose_font)
        toolbar.addWidget(font_btn)
        
        toolbar.addSeparator()
        
        # View buttons
        calendar_btn = QToolButton()
        calendar_btn.setText("Calendar")
        calendar_btn.setToolTip("Calendar View (Ctrl+Shift+C)")
        calendar_btn.clicked.connect(self.show_calendar)
        toolbar.addWidget(calendar_btn)
        
        favorites_btn = QToolButton()
        favorites_btn.setText("Favorites")
        favorites_btn.setToolTip("Show Favorites (Ctrl+Shift+F)")
        favorites_btn.clicked.connect(self.toggle_favorites)
        toolbar.addWidget(favorites_btn)
        
        archived_btn = QToolButton()
        archived_btn.setText("Archived")
        archived_btn.setToolTip("Show Archived (Ctrl+Shift+A)")
        archived_btn.clicked.connect(self.toggle_archived)
        toolbar.addWidget(archived_btn)
        
    def setup_reminder(self, state):
        if not self.current_note:
            self.current_note = Note()
            
        if state == Qt.Checked:
            dialog = QDialog(self)
            dialog.setWindowTitle("Set Reminder")
            dialog.setGeometry(200, 200, 400, 200)
            
            layout = QVBoxLayout()
            
            # Date picker
            date_label = QLabel("Date:")
            date_label.setStyleSheet("color: #ffffff; font-weight: bold;")
            date_picker = QCalendarWidget()
            date_picker.setStyleSheet("""
                QCalendarWidget {
                    background-color: #2d2d2d;
                    color: white;
                    border: 1px solid #3d3d3d;
                    border-radius: 4px;
                }
            """)
            layout.addWidget(date_label)
            layout.addWidget(date_picker)
            
            # Time picker
            time_label = QLabel("Time:")
            time_label.setStyleSheet("color: #ffffff; font-weight: bold;")
            time_edit = QLineEdit()
            time_edit.setText("00:00")
            time_edit.setStyleSheet("""
                QLineEdit {
                    background-color: #2d2d2d;
                    color: white;
                    border: 1px solid #3d3d3d;
                    padding: 8px;
                    border-radius: 4px;
                }
            """)
            layout.addWidget(time_label)
            layout.addWidget(time_edit)
            
            # Buttons
            button_layout = QHBoxLayout()
            
            ok_btn = ModernButton("OK")
            ok_btn.clicked.connect(dialog.accept)
            button_layout.addWidget(ok_btn)
            
            cancel_btn = ModernButton("Cancel")
            cancel_btn.clicked.connect(dialog.reject)
            button_layout.addWidget(cancel_btn)
            
            layout.addLayout(button_layout)
            
            dialog.setLayout(layout)
            
            if dialog.exec_() == QDialog.Accepted:
                date = date_picker.selectedDate()
                time = time_edit.text()
                self.current_note.reminder = datetime.combine(
                    date.toPyDate(),
                    datetime.strptime(time, "%H:%M").time()
                )
                self.statusBar().showMessage(
                    f"Reminder set for {self.current_note.reminder.strftime('%Y-%m-%d %H:%M')}"
                )
        else:
            self.current_note.reminder = None
            self.statusBar().showMessage("Reminder removed")
            
    def handle_attachment(self, state):
        if not self.current_note:
            return
            
        if state:
            # Eklenecek dosyayı seç
            file_path, _ = QFileDialog.getOpenFileName(
                self, 
                "Select File to Attach", 
                "", 
                "All Files (*);;Text Files (*.txt);;Images (*.png *.jpg *.jpeg *.gif);;Documents (*.pdf *.doc *.docx)"
            )
            
            if file_path:
                try:
                    # Dosya ekleme işlemi
                    self.current_note.add_attachment(file_path)
                    
                    # Dosya listesini göster
                    attached_files = [att['name'] for att in self.current_note.attachments]
                    QMessageBox.information(
                        self, 
                        "Attachment Added", 
                        f"Attached file: {os.path.basename(file_path)}\n\nTotal attachments: {len(attached_files)}"
                    )
                    
             
                    self.update_editor()
                    self.save_notes()
                except ValueError as e:
        
                    QMessageBox.warning(self, "Attachment Error", str(e))
                    self.note_editor.attachment_check.setChecked(False)
                except Exception as e:
      
                    QMessageBox.critical(self, "Error", f"Error adding attachment: {str(e)}")
                    self.note_editor.attachment_check.setChecked(False)
        else:

            if self.current_note.attachments:
           
                attachment_names = [att['name'] for att in self.current_note.attachments]
                file_name, ok = QInputDialog.getItem(
                    self, 
                    "Manage Attachments", 
                    "Select attachment to manage:", 
                    attachment_names, 
                    0, 
                    False
                )
                
                if ok and file_name:
       
                    action, ok = QInputDialog.getItem(
                        self, 
                        "Attachment Options", 
                        f"What do you want to do with {file_name}?", 
                        ["View/Open", "Save to disk", "Delete"], 
                        0, 
                        False
                    )
                    
                    if ok:
                        if action == "View/Open":
                   
                            attachment_content = None
                            for att in self.current_note.attachments:
                                if att['name'] == file_name:
                                    attachment_content = att['content']
                                    break
                                    
                            if attachment_content:
                                import base64
                                import tempfile
                                import subprocess
                                import platform
                                
                    
                                temp_dir = tempfile.gettempdir()
                                temp_file_path = os.path.join(temp_dir, file_name)
                                
                                with open(temp_file_path, 'wb') as f:
                                    f.write(base64.b64decode(attachment_content))
                                
                      
                                if platform.system() == 'Windows':
                                    os.startfile(temp_file_path)
                                elif platform.system() == 'Darwin':  # macOS
                                    subprocess.call(['open', temp_file_path])
                                else:  # Linux
                                    subprocess.call(['xdg-open', temp_file_path])
                        
                        elif action == "Save to disk":
          
                            save_path, _ = QFileDialog.getSaveFileName(
                                self, 
                                "Save Attachment", 
                                file_name
                            )
                            
                            if save_path:
                                attachment_content = None
                                for att in self.current_note.attachments:
                                    if att['name'] == file_name:
                                        attachment_content = att['content']
                                        break
                                        
                                if attachment_content:
                                    import base64
                                    with open(save_path, 'wb') as f:
                                        f.write(base64.b64decode(attachment_content))
                                    
                                    QMessageBox.information(
                                        self, 
                                        "Success", 
                                        f"Attachment saved to {save_path}"
                                    )
                        
                        elif action == "Delete":
              
                            reply = QMessageBox.question(
                                self, 
                                "Confirm Delete", 
                                f"Are you sure you want to delete {file_name}?", 
                                QMessageBox.Yes | QMessageBox.No
                            )
                            
                            if reply == QMessageBox.Yes:
                                for i, att in enumerate(self.current_note.attachments):
                                    if att['name'] == file_name:
                                        del self.current_note.attachments[i]
                                        break
                                
                                QMessageBox.information(
                                    self, 
                                    "Success", 
                                    f"Attachment {file_name} deleted."
                                )
                                
                         
                                self.update_editor()
                                self.save_notes()
                
    
                self.note_editor.attachment_check.setChecked(len(self.current_note.attachments) > 0)
            else:
                QMessageBox.information(
                    self, 
                    "No Attachments", 
                    "This note has no attachments."
                )
                self.note_editor.attachment_check.setChecked(False)
        
    def toggle_favorites(self):

        if hasattr(self, 'show_favorites_action'):
            self.show_favorites_action.setChecked(not self.show_favorites_action.isChecked())
        self.filter_notes()
        
    def toggle_archived(self):

        if hasattr(self, 'show_archived_action'):
            self.show_archived_action.setChecked(not self.show_archived_action.isChecked())
        self.filter_notes()
        
    def filter_notes(self):

        search_text = self.search_edit.text().lower() if hasattr(self, 'search_edit') else ""
        selected_tag = self.tag_filter_combo.currentText() if hasattr(self, 'tag_filter_combo') else "All Tags"
        

        show_favorites = self.show_favorites_action.isChecked() if hasattr(self, 'show_favorites_action') else False
        show_archived = self.show_archived_action.isChecked() if hasattr(self, 'show_archived_action') else False
        show_encrypted = self.show_encrypted_action.isChecked() if hasattr(self, 'show_encrypted_action') else False
        

        self.note_list.note_list.clear()
        

        for note in self.notes:
       
            title_match = search_text in note.title.lower()
            content_match = search_text in note.content.lower()
            tags_match = any(search_text in tag.lower() for tag in note.tags)
            search_match = title_match or content_match or tags_match
            
      
            tag_match = (selected_tag == "All Tags" or selected_tag in note.tags)
                

            favorite_match = (not show_favorites or note.is_favorite)
            archived_match = (not show_archived or note.is_archived)
            encrypted_match = (not show_encrypted or note.is_encrypted)
            
    
            if (search_match and tag_match and favorite_match and
                archived_match and encrypted_match):
                item = QListWidgetItem(note.title)
                item.setData(Qt.UserRole, note)
                self.note_list.note_list.addItem(item)
        
   
        self.note_list.update_statistics(self.notes)
        
    def new_note(self):
        self.current_note = Note()
        self.update_editor()
        
    def save_note(self):
        if not self.current_note:
            self.current_note = Note()
            

        title = self.note_editor.title_edit.text().strip()
        if not title:
            QMessageBox.warning(self, "Validation Error", "Title cannot be empty.")
            self.note_editor.title_edit.setFocus()
            return
            
        content = self.note_editor.content_edit.toPlainText().strip()
        if not content:
            QMessageBox.warning(self, "Validation Error", "Content cannot be empty.")
            self.note_editor.content_edit.setFocus()
            return
            
     
        due_date_str = self.note_editor.due_date_edit.text()
        try:
            due_date = datetime.strptime(due_date_str, "%Y-%m-%d %H:%M")
        except ValueError:
            QMessageBox.warning(self, "Validation Error", "Invalid date format. Use YYYY-MM-DD HH:MM format.")
            self.note_editor.due_date_edit.setFocus()
            return
            

        self.current_note.title = title
        self.current_note.content = content
        self.current_note.tags = [tag.strip() for tag in self.note_editor.tags_edit.text().split(",") if tag.strip()]
        self.current_note.priority = self.note_editor.priority_combo.currentText()
        self.current_note.category = self.note_editor.category_combo.currentText()
        self.current_note.due_date = due_date
        self.current_note.is_encrypted = self.note_editor.encrypt_check.isChecked()
        self.current_note.is_favorite = self.note_editor.favorite_check.isChecked()
        self.current_note.is_archived = self.note_editor.archive_check.isChecked()
        self.current_note.modified_at = datetime.now()
        
        # Add or update note in list
        if self.current_note not in self.notes:
            self.notes.append(self.current_note)
            
        self.update_note_list()
        self.update_tag_filter()  
        self.save_notes()
        
        QMessageBox.information(self, "Success", "Note saved successfully!")
        
    def delete_note(self):
        if not self.current_note:
            return
            
        reply = QMessageBox.question(self, "Confirm Delete",
                                   "Are you sure you want to delete this note?",
                                   QMessageBox.Yes | QMessageBox.No)
                                   
        if reply == QMessageBox.Yes:
            self.notes.remove(self.current_note)
            self.current_note = None
            self.update_editor()
            self.update_note_list()
            self.save_notes()
            
    def on_note_selected(self, item):

        if isinstance(item, QListWidgetItem):
            note = item.data(Qt.UserRole)
            if note:
                self.current_note = note
                self.update_editor()
        else:

            self.current_note = item
            self.update_editor()
        
    def update_editor(self):
        if not self.current_note:
            self.note_editor.title_edit.clear()
            self.note_editor.content_edit.clear()
            self.note_editor.tags_edit.clear()
            self.note_editor.priority_combo.setCurrentText("low")
            self.note_editor.category_combo.setCurrentText("general")
            self.note_editor.due_date_edit.setText(datetime.now().strftime("%Y-%m-%d %H:%M"))
            self.note_editor.encrypt_check.setChecked(False)
            self.note_editor.favorite_check.setChecked(False)
            self.note_editor.archive_check.setChecked(False)
            self.note_editor.reminder_check.setChecked(False)
            self.note_editor.attachment_check.setChecked(False)
        else:
            self.note_editor.title_edit.setText(self.current_note.title)
            self.note_editor.content_edit.setText(self.current_note.content)
            self.note_editor.tags_edit.setText(", ".join(self.current_note.tags))
            self.note_editor.priority_combo.setCurrentText(self.current_note.priority)
            self.note_editor.category_combo.setCurrentText(self.current_note.category)
            self.note_editor.due_date_edit.setText(self.current_note.due_date.strftime("%Y-%m-%d %H:%M"))
            self.note_editor.encrypt_check.setChecked(self.current_note.is_encrypted)
            self.note_editor.favorite_check.setChecked(self.current_note.is_favorite)
            self.note_editor.archive_check.setChecked(self.current_note.is_archived)
            self.note_editor.reminder_check.setChecked(self.current_note.reminder is not None)
            self.note_editor.attachment_check.setChecked(len(self.current_note.attachments) > 0)
            
    def update_note_list(self):
        self.note_list.note_list.clear()
        for note in self.notes:
            item = QListWidgetItem(note.title)
            item.setData(Qt.UserRole, note)
            self.note_list.note_list.addItem(item)
            
    def show_calendar(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Calendar View")
        dialog.setGeometry(200, 200, 800, 600)
        
        layout = QVBoxLayout()
        

        calendar_view = CalendarView(dialog)
        calendar_view.update_notes(self.notes)
        layout.addWidget(calendar_view)
        

        note_list_label = QLabel("Notes for Selected Date:")
        note_list_label.setStyleSheet("color: #ffffff; font-weight: bold; font-size: 14px;")
        layout.addWidget(note_list_label)
        

        note_list = QListWidget()
        note_list.setStyleSheet("""
            QListWidget {
                background-color: #2d2d2d;
                color: white;
                border: 1px solid #3d3d3d;
                border-radius: 4px;
                padding: 5px;
            }
            QListWidget::item {
                padding: 8px;
                border-radius: 4px;
            }
            QListWidget::item:selected {
                background-color: #4d4d4d;
                color: white;
            }
            QListWidget::item:hover {
                background-color: #3d3d3d;
            }
        """)
        layout.addWidget(note_list)
        
  
        def on_calendar_date_selected(date):
            note_list.clear()
            selected_date = date.toPyDate()
            for note in self.notes:
                if note.due_date.date() == selected_date:
                    item = QListWidgetItem(note.title)
                    item.setData(Qt.UserRole, note)
                    note_list.addItem(item)
        
        calendar_view.calendar.clicked.connect(on_calendar_date_selected)
        

        def on_note_selected(item):
            note = item.data(Qt.UserRole)
            self.current_note = note
            self.update_editor()
            dialog.accept()
        
        note_list.itemDoubleClicked.connect(on_note_selected)
        

        button_layout = QHBoxLayout()
        
        close_btn = ModernButton("Close")
        close_btn.clicked.connect(dialog.accept)
        button_layout.addWidget(close_btn)
        
        layout.addLayout(button_layout)
        
        dialog.setLayout(layout)
        dialog.exec_()
        
    def backup_notes(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Backup Notes",
                                                 "", "JSON files (*.json)")
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as file:
                    notes_data = [note.to_dict() for note in self.notes]
                    json.dump(notes_data, file, ensure_ascii=False, indent=2)
                QMessageBox.information(self, "Success",
                                      "Notes backed up successfully!")
            except Exception as e:
                QMessageBox.critical(self, "Error",
                                   f"Error during backup: {str(e)}")
                
    def restore_notes(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Restore Notes",
                                                 "", "JSON files (*.json)")
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    notes_data = json.load(file)
                    self.notes = [Note.from_dict(data) for data in notes_data]
                self.update_note_list()
                QMessageBox.information(self, "Success",
                                      "Notes restored successfully!")
            except Exception as e:
                QMessageBox.critical(self, "Error",
                                   f"Error during restore: {str(e)}")
                
    def import_notes(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Import Notes",
                                                 "", "CSV files (*.csv)")
        if file_path:
            try:
                with open(file_path, 'r') as file:
                    reader = csv.DictReader(file)
                    for row in reader:
                        note = Note(
                            title=row['title'],
                            content=row['content'],
                            tags=row['tags'].split(','),
                            priority=row['priority'],
                            due_date=datetime.strptime(row['due_date'],
                                                     "%Y-%m-%d %H:%M"),
                            category=row['category']
                        )
                        self.notes.append(note)
                self.update_note_list()
                self.save_notes()
                QMessageBox.information(self, "Success",
                                      "Notes imported successfully!")
            except Exception as e:
                QMessageBox.critical(self, "Error",
                                   f"Error during import: {str(e)}")
                
    def export_notes(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Export Notes",
                                                 "", "CSV files (*.csv)")
        if file_path:
            try:
                with open(file_path, 'w', newline='') as file:
                    writer = csv.DictWriter(file,
                                          fieldnames=['title', 'content', 'tags',
                                                    'priority', 'due_date',
                                                    'category'])
                    writer.writeheader()
                    for note in self.notes:
                        writer.writerow({
                            'title': note.title,
                            'content': note.content,
                            'tags': ','.join(note.tags),
                            'priority': note.priority,
                            'due_date': note.due_date.strftime("%Y-%m-%d %H:%M"),
                            'category': note.category
                        })
                QMessageBox.information(self, "Success",
                                      "Notes exported successfully!")
            except Exception as e:
                QMessageBox.critical(self, "Error",
                                   f"Error during export: {str(e)}")
                
    def show_about(self):
        QMessageBox.about(self, "About Advanced Notes",
                         "Securonis Notes v1.8\n\n"
                         "A modern note-taking application.\n"
                         "Developed by root0emir")
                         
    def choose_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.note_editor.content_edit.setTextColor(color)
            
    def choose_font(self):
        font, ok = QFontDialog.getFont()
        if ok:
            self.note_editor.content_edit.setFont(font)
            
    def toggle_encryption(self):
        if not self.current_note:
            return
            
        if not self.encryption_key:
            QMessageBox.warning(self, "Warning", 
                              "Encryption key not available. Please restart the application and enter the correct password.")
            return
            
        if not self.current_note.is_encrypted:
            try:
                f = Fernet(self.encryption_key)
                self.current_note.content = f.encrypt(
                    self.current_note.content.encode()).decode()
                self.current_note.is_encrypted = True
                self.statusBar().showMessage("Note encrypted")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Encryption error: {str(e)}")
        else:
            try:
                f = Fernet(self.encryption_key)
                self.current_note.content = f.decrypt(
                    self.current_note.content.encode()).decode()
                self.current_note.is_encrypted = False
                self.statusBar().showMessage("Note decrypted")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Decryption error: {str(e)}")
            
        self.update_editor()
        
    def load_encryption_key(self):
        key_file = 'encryption_key.key'
        

        if os.path.exists(key_file):
   
            password, ok = QInputDialog.getText(
                self, "Enter Password", 
                "Enter encryption password:", 
                QLineEdit.Password
            )
            
            if not ok:
                QMessageBox.warning(self, "Warning", 
                                   "Encryption key not loaded. Some features may not work.")
                self.encryption_key = None
                return
            
            try:
            
                with open(key_file, 'rb') as file:
                    encrypted_key = file.read()
                
     
                import hashlib
              
                key_from_password = hashlib.sha256(password.encode()).digest()
                f = Fernet(Fernet.generate_key())
           
                import base64
                key_bytes = base64.urlsafe_b64decode(encrypted_key)
                
        
                decrypted_key = bytes(a ^ b for a, b in zip(key_bytes, key_from_password))
                
        
                try:
                    Fernet(decrypted_key)
                    self.encryption_key = decrypted_key
                except Exception:
                    QMessageBox.critical(self, "Error", "Invalid password or corrupted key.")
                    self.encryption_key = None
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error loading encryption key: {str(e)}")
                self.encryption_key = None
        else:
            while True:
                password, ok = QInputDialog.getText(
                    self, "Create Password", 
                    "Create encryption password (min 8 chars):", 
                    QLineEdit.Password
                )
                
                if not ok:
            
                    self.encryption_key = Fernet.generate_key()
                    QMessageBox.warning(self, "Warning", 
                                       "Using default encryption. Notes will not be securely encrypted.")
                    break

                if len(password) < 8:
                    QMessageBox.warning(self, "Warning", "Password must be at least 8 characters.")
                    continue
                
                confirm, ok = QInputDialog.getText(
                    self, "Confirm Password", 
                    "Confirm encryption password:", 
                    QLineEdit.Password
                )
                
                if not ok or password != confirm:
                    QMessageBox.warning(self, "Warning", "Passwords don't match. Try again.")
                    continue
                
  
                self.encryption_key = Fernet.generate_key()
                

                import hashlib
 
                key_from_password = hashlib.sha256(password.encode()).digest()
                
      
                key_bytes = base64.urlsafe_b64decode(self.encryption_key)
                encrypted_key = bytes(a ^ b for a, b in zip(key_bytes, key_from_password))
                
        
                with open(key_file, 'wb') as file:
                    file.write(base64.urlsafe_b64encode(encrypted_key))
                
                QMessageBox.information(self, "Success", 
                                       "Encryption key created and secured with your password.")
                break
                
    def check_reminders(self):

        current_time = datetime.now()
        for note in self.notes:
            if note.reminder and note.reminder <= current_time:
     
                QMessageBox.information(self, "Hatırlatıcı", 
                                       f"Not: {note.title}\n\n{note.content}")
       
                note.reminder = None
                self.save_notes()
        
    def load_notes(self):
        try:
            if os.path.exists('notes.json'):
                with open('notes.json', 'r', encoding='utf-8') as file:
                    notes_data = json.load(file)
                    self.notes = [Note.from_dict(data) for data in notes_data]
                self.update_note_list()
                self.update_tag_filter()  
                self.update_category_combo()
                self.statusBar().showMessage(f"{len(self.notes)} notes loaded.")
            else:
                self.statusBar().showMessage("Note file not found. You can create new notes.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error loading notes: {str(e)}")
            
    def save_notes(self):
        try:
            with open('notes.json', 'w', encoding='utf-8') as file:
                notes_data = [note.to_dict() for note in self.notes]
                json.dump(notes_data, file, ensure_ascii=False, indent=2)
            self.statusBar().showMessage(f"{len(self.notes)} notes saved.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error saving notes: {str(e)}")
            
    def closeEvent(self, event):
        try:
            self.save_notes()

            if hasattr(self, 'reminder_timer'):
                self.reminder_timer.stop()
            event.accept()
        except Exception as e:
     
            with open('error.log', 'a') as f:
                import datetime
                f.write(f"\n[{datetime.datetime.now()}] Error during close: {str(e)}\n")
            event.accept()  

    def add_note(self, note):
  
        self.notes.append(note)
        self.current_note = note
        self.update_note_list()
        self.save_notes()
        self.statusBar().showMessage(f"Note added: {note.title}")

    def update_tag_filter(self):

        current_tag = self.tag_filter_combo.currentText()
        self.tag_filter_combo.clear()
        self.tag_filter_combo.addItem("All Tags")
        
   
        all_tags = set()
        for note in self.notes:
            all_tags.update(note.tags)
        
 
        for tag in sorted(all_tags):
            self.tag_filter_combo.addItem(tag)
            
   
        index = self.tag_filter_combo.findText(current_tag)
        if index >= 0:
            self.tag_filter_combo.setCurrentIndex(index)

    def manage_categories(self):
        all_categories = set()
        for note in self.notes:
            all_categories.add(note.category)
        

        dialog = CategoryManager(self, list(all_categories))
        if dialog.exec_() == QDialog.Accepted:

            updated_categories = dialog.get_categories()
            
  
            category_map = {}
            for old_cat in all_categories:
                if old_cat not in updated_categories:
  
                    new_cat, ok = QInputDialog.getItem(
                        self, "Update Category", 
                        f"Category '{old_cat}' was removed. Map notes to:",
                        updated_categories, 0, False
                    )
                    if ok:
                        category_map[old_cat] = new_cat
                    else:
                        category_map[old_cat] = "general"  
            
       
            for note in self.notes:
                if note.category in category_map:
                    note.category = category_map[note.category]
            
   
            self.note_editor.category_combo.clear()
            for category in sorted(updated_categories):
                self.note_editor.category_combo.addItem(category)
            
    
            self.update_note_list()
            self.save_notes()
    
    def manage_tags(self):

        all_tags = set()
        for note in self.notes:
            all_tags.update(note.tags)
        

        dialog = TagManager(self, list(all_tags))
        if dialog.exec_() == QDialog.Accepted:
    
            updated_tags = dialog.get_tags()
            
           
            self.update_tag_filter()

    def update_category_combo(self):

        categories = set()
        categories.add("general")  
        categories.add("work")
        categories.add("personal")
        categories.add("ideas")
        categories.add("tasks")
        
  
        for note in self.notes:
            if note.category:
                categories.add(note.category)
                

        current_category = self.note_editor.category_combo.currentText()
        self.note_editor.category_combo.clear()
        

        for category in sorted(categories):
            self.note_editor.category_combo.addItem(category)
            

        index = self.note_editor.category_combo.findText(current_category)
        if index >= 0:
            self.note_editor.category_combo.setCurrentIndex(index)
    
    def load_notes(self):
        try:
            if os.path.exists('notes.json'):
                with open('notes.json', 'r', encoding='utf-8') as file:
                    notes_data = json.load(file)
                    self.notes = [Note.from_dict(data) for data in notes_data]
                self.update_note_list()
                self.update_tag_filter()  
                self.update_category_combo()  
                self.statusBar().showMessage(f"{len(self.notes)} notes loaded.")
            else:
                self.statusBar().showMessage("Note file not found. You can create new notes.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error loading notes: {str(e)}")

def handle_exception(exctype, value, traceback):

    error_message = f"{exctype.__name__}: {value}"
    print(f"Error occurred: {error_message}")
    

    app = QApplication.instance()
    for widget in app.topLevelWidgets():
        if isinstance(widget, QMainWindow):
            QMessageBox.critical(widget, "Error", 
                               f"An unexpected error occurred:\n\n{error_message}\n\nThe application will try to continue.")
       
            try:
                with open('error.log', 'a') as f:
                    import datetime
                    f.write(f"\n[{datetime.datetime.now()}] {error_message}\n")
                    import traceback as tb
                    tb.print_exc(file=f)
            except:
                pass
            break
    
    sys.__excepthook__(exctype, value, traceback)

def main():
    app = QApplication(sys.argv)
    
    sys.excepthook = handle_exception
    
    # Set application style
    app.setStyle('Fusion')
    
    # Create dark palette with modern colors
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(30, 30, 30))
    palette.setColor(QPalette.WindowText, Qt.white)
    palette.setColor(QPalette.Base, QColor(25, 25, 25))
    palette.setColor(QPalette.AlternateBase, QColor(35, 35, 35))
    palette.setColor(QPalette.ToolTipBase, Qt.white)
    palette.setColor(QPalette.ToolTipText, Qt.white)
    palette.setColor(QPalette.Text, Qt.white)
    palette.setColor(QPalette.Button, QColor(35, 35, 35))
    palette.setColor(QPalette.ButtonText, Qt.white)
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.HighlightedText, Qt.black)
    app.setPalette(palette)
    

    app.setFont(QFont("Segoe UI", 9))
    
    try:
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
 
        QMessageBox.critical(None, "Critical Error", 
                           f"A critical error occurred during startup:\n\n{str(e)}\n\nThe application will now exit.")

        try:
            with open('critical_error.log', 'a') as f:
                import datetime
                f.write(f"\n[{datetime.datetime.now()}] Critical Error: {str(e)}\n")
                import traceback
                traceback.print_exc(file=f)
        except:
            pass
        sys.exit(1)

if __name__ == "__main__":
    main() 
