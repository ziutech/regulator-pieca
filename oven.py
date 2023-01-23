import pandas as pd


sampling_rate: float = 0.01  # T_p
sim_time: float = 800

current_min, current_max = 0, 11
control_variable_min, control_variable_max = 2.5, 7.5

C_wp = 713
m_p = 0.5 * 0.5 * 0.5 * 1.1225
C_wg = 460
m_g = 1

h = 50
A = 0.12
A_ = 6 * 0.5 * 0.5

U = 230
R_r = 8.64
R_a = 0.24
C_s = 8.8
C_r = 10.164
temp_o = 20

a = (current_max - current_min) / (control_variable_max - control_variable_min)


def p(T_s, T_g, T_r, T_a, I):
    T_g = 0.8 * U * I / (C_wg * m_g)
    q = h * A * (T_g - T_s)
    q_r = R_r * (T_a - T_r)
    q_a = R_a * (T_r - T_a)
    T_r = T_r + (q_r - q_a) / C_r * sampling_rate
    T_s = T_s + (q - q_r) / C_s * sampling_rate
    return T_s, T_g, T_r


def simulate(goal_temp, k_p, T_i, T_d, **kwargs):
    # def bound(v, v_min, v_max) -> float:
    #     return max(v_min, min(v, v_max))

    t = [0.0]
    control_variable = [0.0]
    e = [0.0]
    de = [0.0]

    temp = [20.0]
    goal_temp = [goal_temp]
    temp_r = [20.0]
    temp_g = [20.0]
    current = [0.0]

    for n in range(1, int(sim_time / sampling_rate) + 1):
        t.append(n * sampling_rate)

        e.append(goal_temp[-1] - temp[-1])
        de.append(e[-1] - e[-2])

        # e[-1] - e[-2] + sampling_rate / T_i * e[-2]
        P = e[-1] - e[-2]
        I = sampling_rate / T_i * e[-1]
        D = T_d / sampling_rate * (de[-1] - de[-2])
        control_variable.append(
            (P + I + D) * k_p + control_variable[-1],
        )

        # current.append(bound(a * (control_variable[-1] - control_variable_min) + current_min, current_min, current_max))
        current.append(a * (control_variable[-1] - control_variable_min) + current_min)

        T, T_g, T_r = p(temp[-1], temp_g[-1], temp_r[-1], temp_o, current[-1])

        temp.append(T)
        temp_g.append(T_g)
        temp_r.append(T_r)

        # temp.append(
        #     (C_wp * m_p / sampling_rate * temp_tmp[-1] - h * A_ * temp_o)
        #     / (C_wp * m_p / sampling_rate - h * A_)
        # )

    return pd.DataFrame(
        data={"czas": t, "temperatura": temp, "temp_r": temp_r, "temp_g": temp_g}
    )


#
