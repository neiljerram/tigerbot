package main

import (
	"fmt"
	"time"

	"github.com/tigerbot-team/tigerbot/go-controller/pkg/joystick"
	"github.com/tigerbot-team/tigerbot/go-controller/pkg/propeller"
)

func main() {
	fmt.Print("---- Tigerbot ----\n\n")


restartLoop:
	for {
		p, err := propeller.New()
		if err != nil {
			fmt.Printf("Failed to open propeller: %v.\n", err)
			time.Sleep(1 * time.Second)
			continue
		}
		for {
			fmt.Println("Front left")
			err = p.SetMotorSpeeds(2, 0, 0, 0)
			if err != nil {
				panic(err)
			}
			time.Sleep(1*time.Second)
			fmt.Println("Front right")
			err = p.SetMotorSpeeds(0, 2, 0, 0)
			if err != nil {
				panic(err)
			}
			time.Sleep(1*time.Second)
			fmt.Println("Back left")
			err = p.SetMotorSpeeds(0, 0, 2, 0)
			if err != nil {
				panic(err)
			}
			time.Sleep(1*time.Second)
			fmt.Println("Back right")
			err = p.SetMotorSpeeds(0, 0, 0, 2)
			if err != nil {
				panic(err)
			}
			time.Sleep(1*time.Second)


			fmt.Println("Turning off motors")
			err = p.SetMotorSpeeds(0,0, 0, 0)
			if err != nil {
				panic(err)
			}
			time.Sleep(5*time.Second)
		}


		j, err := joystick.NewJoystick("/dev/input/js0")
		if err != nil {
			fmt.Printf("Failed to open joystick: %v.\n", err)
			time.Sleep(1 * time.Second)
			continue
		}
		for {
			event, err := j.ReadEvent()
			if err != nil {
				j.Close()
				fmt.Printf("Failed to read from joystick: %v.\n", err)
				time.Sleep(1 * time.Second)
				continue restartLoop
			}
			fmt.Printf("Event from joystick: %s\n", event)
		}
	}
}
