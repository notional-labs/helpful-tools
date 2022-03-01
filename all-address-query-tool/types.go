package main

type Packet_balance_success struct {
	Balances []struct {
		Denom  string `json:"denom"`
		Amount string `json:"amount"`
	} `json:"balances"`
	Pagination struct {
		Next_key string `json:"next_key"`
		Total    string `json:"total"`
	} `json:"pagination"`
}

type Packet_accounts_success struct {
	Accounts []struct {
		Type    string `json:"@type"`
		Address string `json:"address"`
		Pub_key struct {
			Type string `json:"@type"`
			Key  string `json:"key"`
		} `json:"pub_key"`
		Account_number string `json:"account_number"`
		Sequence       string `json:"sequence"`
	} `json:"accounts"`
	Pagination struct {
		Next_key string `json:"next_key"`
		Total    string `json:"total"`
	} `json:"pagination"`
}
