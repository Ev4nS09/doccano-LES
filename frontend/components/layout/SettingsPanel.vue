<template>
	<v-dialog v-model="isVisible" persistent max-width="600px">
		<v-card>
			<v-card-title class="headline">
				Profile Settings
			</v-card-title>

			<!-- Botões para alternar entre Nome e Senha -->
			<v-btn-toggle v-model="selectedCategory" mandatory>
				<v-btn value="name" :class="{ 'primary--text': selectedCategory === 'name' }">
					Change Profile
				</v-btn>
				<v-btn value="password" :class="{ 'primary--text': selectedCategory === 'password' }">
					{{ $t('user.changePassword') }}
				</v-btn>
			</v-btn-toggle>

			<v-divider></v-divider>

			<!-- Formulário -->
			<v-card-text>
				<v-form ref="form" v-model="isFormValid">
					<!-- Alteração de Nome -->
					<div v-if="selectedCategory === 'name'">
						<v-row dense>
							<v-col cols="6">
								<v-text-field class="change-first-name" v-model="firstName" 
									label="First Name" 
									outlined 
									dense
									:rules="[rules.firstNameRequired]"></v-text-field>
							</v-col>

							<v-col cols="6">
								<v-text-field class="change-last-name" v-model="lastName" 
									label="Last Name" 
									outlined 
									dense
									:rules="[rules.lastNameRequired]"></v-text-field>
							</v-col>
						</v-row>
							
						<v-text-field class="change-username" v-model="username" 
							:label="$t('user.username')" 
							outlined 
							dense
							:rules="[rules.userRequired]"></v-text-field>

						<v-text-field class="change-email" v-model="email" 
							label="Email" 
							outlined 
							dense
							:rules="[rules.emailRequired, rules.validEmail]"></v-text-field>

					</div>

					<!-- Alteração de Senha -->
					<div class="change-password" v-else>
						<v-text-field v-model="oldPassword" :label="$t('user.oPassword')" 
						type="password" 
						outlined 
						dense
							:rules="[rules.passwordRequired, rules.minPassword]"></v-text-field>

						<!-- Divider for separation -->
						<v-divider class="my-4"></v-divider>

						<v-text-field v-model="newPassword" :label="$t('user.nPassword')" 
						type="password" 
						outlined 
						dense
							:rules="[rules.passwordRequired, rules.minPassword]"></v-text-field>

						<v-text-field v-model="confirmPassword" 
						:label="$t('user.cPassword')" 
						type="password" 
						outlined
							dense :rules="[rules.passwordRequired, rules.passwordMatch]"></v-text-field>
					</div>
				</v-form>
			</v-card-text>

			<v-card-actions>
				<v-spacer></v-spacer>
				<v-btn text @click="closePanel">{{ $t('generic.cancel') }}</v-btn>
				<v-btn color="primary" :disabled="!isFormValid" @click="submitSettings">
					{{ $t('generic.save') }}
				</v-btn>
			</v-card-actions>
		</v-card>
	</v-dialog>
</template>

<script>
import { mapActions, mapGetters } from 'vuex'

export default {
	data() {
		return {
			isVisible: false,
			username: '',
			firstName: '',
            lastName: '',
			email: '',
			oldPassword: '',
			newPassword: '',
			confirmPassword: '',
			isFormValid: false,
			selectedCategory: 'name', // 'name' ou 'password'
			rules: {
				userRequired: value => !!value || this.$i18n.t('rules.userNameRules.userNameRequired'),
				firstNameRequired: value => !!value || 'First name required',
				lastNameRequired: value => !!value || 'Last name required',
				passwordRequired: value => !!value || this.$i18n.t('rules.passwordRules.passwordRequired'),
				minPassword: value => value.length >= 6 || this.$i18n.t('rules.passwordRules.passwordMoreThan6Chars'),
				passwordMatch: value => value === this.newPassword || this.$i18n.t('rules.passwordRules.passwordMatch'),
				emailRequired: value => !!value || 'Email required',
				validEmail: value => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value) || 'Invalid email',
			},
		};
	},
	computed: {
		...mapGetters('auth', ['getUsername', 'getEmail', 'getFirstName', 'getLastName']),
	},
	watch: {
		getUsername(newUsername) {
			if (newUsername) {
				this.username = newUsername.username || '';
			}
		},
		getEmail(newEmail) {
			if (newEmail) {
				this.email = newEmail.email || '';
			}
		},
		getFirstName(newFirstName) {
			if (newFirstName) {
				this.firstName = newFirstName.firstName || '';
			}
		},
		getLastName(newLastName) {
			if (newLastName) {
				this.lastName = newLastName.lastName || '';
			}
		},
	},
	methods: {
		...mapActions('auth', ['updateUsername', 'updatePassword', 'updateEmail', 'updateFirstName', 'updateLastName']),

		openPanel() {
			this.isVisible = true;
			console.log("getUsername:", this.getUsername); // Verifica o que está a ser retornado
			console.log("getEmail:", this.getEmail);

			if (this.getUsername) {
				this.username = this.getUsername || ''; 
			} else {
				this.username = ''; 
			}

			if (this.getEmail) {
				this.email = this.getEmail || ''; 
			} else {
				this.email = ''; 
			}

			if (this.getFirstName) {
				this.firstName = this.getFirstName || ''; 
			} else {
				this.firstName = ''; 
			}

			if (this.getLastName) {
				this.lastName = this.getLastName || ''; 
			} else {
				this.lastName = ''; 
			}
		},
		closePanel() {
			this.isVisible = false;
			this.username = this.getUsername;
			this.firstName = this.getFirstName || '';
            this.lastName = this.getLastName || '';
			this.oldPassword = '';
			this.newPassword = '';
			this.confirmPassword = '';
			this.selectedCategory = 'name';
			this.email = this.getEmail;
		},

		async submitSettings() {
			if (this.$refs.form.validate()) {
				if (this.selectedCategory === 'name') {
					
					if (this.username !== this.getUsername) { // Apenas atualiza se houver mudança
						try {
							await this.updateUsername(this.username);
							this.username = this.getUsername
							alert("Username updated successfully!");
						} catch (error) {
						}
					}
					if (this.email !== this.getEmail) {
						try {
                            await this.updateEmail(this.email);
                            alert("Email updated successfully!");
                        } catch (error) {
                        }
					}
					if (this.firstName !== this.getFirstName) {
                        try {
                            await this.updateFirstName(this.firstName);
                            alert("First name updated successfully!");
                        } catch (error) {
                        }
                    }
                    if (this.lastName !== this.getLastName) {
                        try {
                            await this.updateLastName(this.lastName);
                            alert("Last name updated successfully!");
                        } catch (error) {
                        }
                    }
				} else {
					try {
						await this.updatePassword({
							oldPassword: this.oldPassword,
							newPassword: this.newPassword
						});
					} catch (error) {
						if (error.response != null) {
							alert(error.response);
						} else {
							alert("Error updating password: Old password is incorrect!");
						}
					}
				}
				this.closePanel();
			}
		}
	}
};
</script>

<style scoped>
.v-dialog__content {
	backdrop-filter: none;
	/* Remover o desfoque de fundo */
}

.v-card {
	border-radius: 10px;
}

.v-card-title {
	margin-bottom: 15px;
}

.v-btn {
	font-weight: bold;
}

.v-divider {
	margin: 16px 0px;
}

.v-btn-toggle {
	width: 100%;
	display: flex;
	justify-content: stretch;
	padding: 0px 20px;
}

.v-btn-toggle .v-btn {
	flex: 1;
	font-weight: bold;
}

.primary--text {
	color: #1976d2 !important;
}

</style>
