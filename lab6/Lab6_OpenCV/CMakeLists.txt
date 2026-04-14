cmake_minimum_required(VERSION 3.10)
project(Lab6_OpenCV)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Пошук OpenCV
find_package(OpenCV REQUIRED)

# Додавання директорії з заголовними файлами
include_directories(include ${OpenCV_INCLUDE_DIRS})

# Пошук всіх вихідних файлів
file(GLOB SOURCES "src/*.cpp")

# Створення виконуваного файлу
add_executable(${PROJECT_NAME} ${SOURCES})

# Лінковка з OpenCV
target_link_libraries(${PROJECT_NAME} ${OpenCV_LIBS})
