extends Node2D

var line_edit: LineEdit
var label: Label

func _ready():
	line_edit = $LineEdit
	label = $Label
	
	line_edit.connect("text_entered", self, "_on_LineEdit_text_entered")

func _on_LineEdit_text_entered(new_text):
	label.text = new_text
