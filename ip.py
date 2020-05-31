import ipaddress
import sys


def first_dif_octet(address1, address2):
    for index, (octet1, octet2) in enumerate(zip(address1.packed, address2.packed)):
        if octet1 != octet2:
            return index


def octet_mask_len(octet1, octet2):
    for index, (bit1, bit2) in enumerate(zip(bin(octet1)[2:].zfill(8), bin(octet2)[2:].zfill(8))):
        if (bit1 != bit2):
            return index


def find_subnet(address1, address2):
    diff_octet = first_dif_octet(address1, address2)
    if diff_octet is None:
        return ipaddress.ip_network(address1)
    mask_len = 0
    for i in range(4):
        if i < diff_octet:
            mask_len += 8
        elif i == diff_octet:
            mask_len += octet_mask_len(address1.packed[diff_octet], address2.packed[diff_octet])
        else:
            break
    return ipaddress.ip_network('{}/{}'.format(address1, mask_len), strict=False)


def find_min_subnet(addresses):
    if len(addresses) == 0:
        return None
    elif len(addresses) == 1:
        return ipaddress.ip_network(addresses[0])
    elif len(addresses) == 2:
        return find_subnet(addresses[0], addresses[1])
    else:
        subnet = find_subnet(addresses[0], addresses[1])
        for address in addresses[2:]:
            new_subnet = find_subnet(
                next(subnet.hosts()) if subnet.network_address != subnet.broadcast_address else subnet.network_address,
                address)
            if new_subnet < subnet:
                subnet = new_subnet
        return subnet


if __name__ == '__main__':
    try:
        addresses = list(map(lambda address: ipaddress.ip_address(address), open(sys.argv[1], 'r').read().splitlines()))
        print(find_min_subnet(addresses))
    except BaseException as err:
        print(err)
        exit(1)
