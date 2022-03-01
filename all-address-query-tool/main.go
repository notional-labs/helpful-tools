package main

import (
	"encoding/csv"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"os"
	"strconv"
)

const (
	API = "https://api.stars.kingnodes.com"
)

var (
	GET_ALL_ACCOUNT_API     = API + "/cosmos/auth/v1beta1/accounts?pagination.key=%s"
	GET_BALANCE_ACCOUNT_API = API + "/cosmos/bank/v1beta1/balances/%s"
)

func main() {
	// get data from API server
	pagination_key := ""

	for true {
		// get GET data
		resp, err := http.Get(fmt.Sprintf(GET_ALL_ACCOUNT_API, pagination_key))
		if err != nil {
			fmt.Printf("Unable to get pagination key = %s \n", pagination_key)
		}

		defer resp.Body.Close()
		body, err := ioutil.ReadAll(resp.Body)
		var result Packet_accounts_success
		if err := json.Unmarshal(body, &result); err != nil { // Parse []byte to go struct pointer
			log.Fatalf("ERROR: Can not unmarshal JSON packet addresses at pagination_key = %s with string = %s \n", pagination_key, string(body))
		}

		pagination_key = result.Pagination.Next_key

		// write data down to a file as csv
		for _, s := range result.Accounts {
			balance, err := GetAccountBalance(s.Address)
			if err != nil {
				fmt.Println(err)
				continue
			}

			err = WriteBalanceToCsv([][]string{{s.Address, balance}})
			if err != nil {
				log.Panic(err)
			}
		}
	}

}

func GetAccountBalance(address string) (string, error) {
	resp, err := http.Get(fmt.Sprintf(GET_BALANCE_ACCOUNT_API, address))
	if err != nil {
		return "", fmt.Errorf("Unable to get %s \n", address)
	}

	defer resp.Body.Close()
	body, err := ioutil.ReadAll(resp.Body)
	var result Packet_balance_success
	if err := json.Unmarshal(body, &result); err != nil { // Parse []byte to go struct pointer
		return "", fmt.Errorf("ERROR: Can not unmarshal JSON packet balance with string = %s \n", string(body))
	}

	// assume that first position is chain's denom

	// IF THERE IS ANY FILTER, WRITE IT HERE
	if len(result.Balances) == 0 {
		return "", fmt.Errorf("ERROR: address %s doesn't have balances \n", address)
	}

	amount_uint, err := strconv.ParseUint(result.Balances[0].Amount, 10, 64)

	if amount_uint <= 100 {
		return "", fmt.Errorf("ERROR: address %s has < 100 starz \n", address)
	}

	return fmt.Sprintf("%s%s", result.Balances[0].Amount, result.Balances[0].Denom), nil
}

func WriteBalanceToCsv(data [][]string) error {
	file, err := os.OpenFile("data/balances.csv", os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
	if err != nil {
		return fmt.Errorf(err.Error())
	}
	defer file.Close()

	writer := csv.NewWriter(file)
	defer writer.Flush()

	for _, value := range data {
		err := writer.Write(value)
		if err != nil {
			return fmt.Errorf(err.Error())
		}
	}

	return nil
}
