use std::{
    io::{self, Write},
    process, thread,
    time::Duration,
};

// you can safely ignore all these fancy display functions
fn slow_print(text: &str) {
    for c in text.chars() {
        print!("{}", c);
        io::stdout().flush().unwrap();
        thread::sleep(Duration::from_millis(10));
    }
    println!();
}

fn show_welcome() {
    let forest = r#"_____________________________________
|      ___                          |
|    _(   )__      ____             |
|   (_       )   _(   _)_    __     |
|) (_         ) (_       )_ (  )_   |
| ) (___, :__) )_(__| :__) )     )  |
|)      | | (_ ,_)  | |     (_||_)  |
|_      | |   ||    | / ___________ |
| )_    \ |  _j|_   | | |         | |
| __)  _j |__    ___j |_| (@ @ @) | |
| _        __j__        | (o o o) | |
|_,   _l___   (  )  __  |      O  | |
|    __      (___)  l___|  _____  | |
|   _.  ___    ,__    __| |_____| | |
"#;
    println!("\n{}", forest);
    slow_print("Wandering in the forest, you spot a rusty vending machine...");
}

fn show_display(balance: u32) {
    println!("Balance: {}", balance);
    let display = r#"______________________________________

       🪴       🍕       🚩
     O 13      O 11    O 1000000
       
______________________________________

                   __________
                  (__________)   O
"#;
    println!("\n{}", display);
}

// aight start reading from here
fn check_balance(balance: u32, amount: u32) -> bool {
    // return !(balance - amount >= 0); (ok changing this, might int underflow)
    return balance >= amount;
}

fn main() {
    let mut balance: u32 = 100; // Free money for you at the start :)
    const FLAG: &str = "grey{bUt_h3y_a_f1aG_1s_4_Fl4g!}";
    let mut coin_eaten: bool = false;

    show_welcome();

    loop {
        show_display(balance);
        println!("(1) Insert Coin");
        println!("(2) Insert Notes");
        println!("(0) Leave");
        // get user input
        let mut input: String = String::new();
        io::stdin().read_line(&mut input).unwrap();
        let choice: u32 = input.trim().parse::<u32>().unwrap_or(0);
        match choice {
            1 => {
                if coin_eaten {
                    slow_print("The machine already ate your coin, don't do it again ._.");
                } else {
                    slow_print("And.... nothing happens. The machine ate your coin :((");
                    balance = balance - 1;
                    coin_eaten = true;
                }
            }
            2 => {
                println!("What would you like to buy?");
                println!("(1) Potted Plant 🪴 - 13 coins");
                println!("(2) Mystery Pizza 🍕 - 11 coins");
                println!("(3) Flag 🚩 - 1,000,000 coins");
                println!("(0) Ask for change (go back)");
                let mut input: String = String::new();
                io::stdin().read_line(&mut input).unwrap();
                let choice: u32 = input.trim().parse::<u32>().unwrap_or(0);
                match choice {
                    1 => {
                        if check_balance(balance, 13) {
                            slow_print("You bought a Potted Plant! 🪴");
                            slow_print("Why'd you even do that, there's plants all around you...");
                            balance = balance - 13;
                        } else {
                            println!("You don't have enough coins for that.");
                        }
                    }
                    2 => {
                        if check_balance(balance, 11) {
                            slow_print("You bought a Mystery Pizza! 🍕");
                            slow_print(
                                "You take a look at it and realise it's expired. Please don't eat it...",
                            );
                            balance = balance - 11;
                        } else {
                            println!("You don't have enough coins for that.");
                        }
                    }
                    3 => {
                        if check_balance(balance, 1000000) {
                            slow_print("You bought a Flag! 🚩");
                            slow_print("The flag looks mouldy, probably from years of storage...");
                            slow_print(FLAG);
                            process::exit(0);
                        } else {
                            println!("You don't have enough coins for that.");
                        }
                    }
                    0 => {
                        continue;
                    }
                    _ => {
                        println!("Hmm, that isn't right, try again.");
                    }
                }
            }
            0 => {
                // Leave
                slow_print("The machine rattles and makes a weird noise as you walk away...");
                process::exit(0);
            }
            _ => {
                println!("Hmm, that isn't right, try again.");
            }
        }
    }
}
