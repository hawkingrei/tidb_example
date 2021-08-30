package main

import (
	"gorm.io/driver/mysql"
	"gorm.io/gorm"
)

type Order struct {
	gorm.Model
	ID       int     `gorm:"primary_key,autoIncrement"`
	Username string  `gorm:"column:username"`
	Price    float64 `gorm:"column:price"`
}

func main() {
	dsn := "root:@tcp(localhost:4000)/gorm?charset=utf8&parseTime=True&loc=Local"
	db, err := gorm.Open(mysql.Open(dsn), &gorm.Config{})
	if err != nil {
		panic("failed to connect database")
	}

	// Create table
	db.AutoMigrate(&Order{})

	// Insert
	db.Create(&Order{Username: "a", Price: 100})
	db.Create(&Order{Username: "b", Price: 200})
	db.Create(&Order{Username: "c", Price: 200})

	// Delete
	db.Delete(&Order{}, 1)
	db.Where("Username = ?", "c").Delete(&Order{})

	// Update
	db.Model(&Order{}).Where("id = ?", 2).Update("Username", "hello")

}
