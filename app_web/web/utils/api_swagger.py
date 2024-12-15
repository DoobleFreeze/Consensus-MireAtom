template = {
    'openapi': '3.0.3',
    "info": {
        "title": "Consensus API",
        "description": "API для работы со формулами.",
        "version": "1.0.0"
    },
    "tags": [
        {
            "name": "Сравнение формул",
            "description": "Сравнение формулы с данными из БД"
        },
        {
            "name": "Работа с БД",
            "description": "Взаимодействие с базой данных"
        }
    ],
    "components": {
        "schemas": {
            "Success": {
                "type": "object",
                "properties": {
                    "result": {
                        "type": "object",
                        "example": "[[90, ['a', 'a']], [90, ['a', 'a']], [90, ['a', 'a']]]"
                    },
                },
                "required": [
                    "result",
                    "success"
                ]
            },
            "Input": {
                "type": "object",
                "properties": {
                    "formula": {
                        "type": "string",
                        "example": "какой-то текст"
                    },
                },
                "required": [
                    "text",
                ]
            },
        }
    },
    "paths": {
        "/api/diff_formula": {
            "post": {
                "tags": ["Сравнение формул"],
                "summary": "Сравнение формулы с БД",
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {
                                "$ref": '#/components/schemas/Input'
                            }
                        }
                    }
                },
                "responses": {
                    "200": {
                        "description": "Сравнение формул прошло успешно",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": '#/components/schemas/Success'
                                }
                            }
                        }
                    },
                }
            }
        },
        "/api/add_formula": {
            "post": {
                "tags": ["Работа с БД"],
                "summary": "Добавление новой формулы в БД",
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {
                                "$ref": '#/components/schemas/Input'
                            }
                        }
                    }
                },
                "responses": {
                    "200": {
                        "description": "Формула добавлена",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": '#/components/schemas/Success'
                                }
                            }
                        }
                    },
                }
            }
        },
        "/api/database": {
            "get": {
                "tags": ["Работа с БД"],
                "summary": "Выгрузить данные из БД",
                "responses": {
                    "200": {
                        "description": "Данные выгружены",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": '#/components/schemas/Success'
                                }
                            }
                        }
                    },
                }
            }
        },
    }
}
