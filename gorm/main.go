package main

import (
	"fmt"

	"gorm.io/driver/mysql"
	"gorm.io/gorm"
)

type Order struct {
	gorm.Model
	ID       int     `gorm:"primary_key,autoIncrement"`
	Username string  `gorm:"column:username"`
	Price    float64 `gorm:"column:price"`
}

func PrintResult(tx *gorm.DB, result []Order) {
	if tx.Error == nil && tx.RowsAffected > 0 {
		for _, order := range result {
			fmt.Printf("%+v\n", order)
		}
	}
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
	db.Create(&Order{Username: "c", Price: 300})
	db.Create(&Order{Username: "d", Price: 400})
	db.Create(&Order{Username: "e", Price: 500})

	// Delete
	db.Delete(&Order{}, 1)
	db.Where("Username = ?", "c").Delete(&Order{})

	// Update
	db.Model(&Order{}).Where("id = ?", 2).Update("Username", "hello")

	var orders []Order
	// Get all records
	result := db.Find(&orders)
	PrintResult(result, orders)

	// Get records with conditions
	result = db.Where("username IN ?", []string{"b", "c", "d", "e"}).Find(&orders)
	PrintResult(result, orders)

	result = db.Where("price >= ?", 300).Find(&orders)
	PrintResult(result, orders)

	result = db.Raw("SELECT * FROM orders WHERE price = ?", 500).Scan(&orders)
	PrintResult(result, orders)
}
