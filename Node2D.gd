extends Node2D

@onready var line_edit: LineEdit = $LineEdit
@onready var label: Label = $Label

# Called when the node enters the scene tree for the first time.
func _ready():
	line_edit.text_submitted.connect(_on_LineEdit_text_entered)

func _on_LineEdit_text_entered(new_text: String) -> void:
	label.text = "your txt :" + new_text
